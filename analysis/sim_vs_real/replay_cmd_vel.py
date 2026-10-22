#!/usr/bin/env python3
"""Read a CSV command recording; dry-run by default, opt-in ROS 2 sim replay."""
import argparse
import csv
import math
import os
import time


def read_commands(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not {"t_s","linear_x","angular_z"}.issubset(set(reader.fieldnames or [])):
            raise ValueError("Command CSV needs t_s,linear_x,angular_z")
        rows = [(float(r["t_s"]),float(r["linear_x"]),float(r["angular_z"]))
                for r in reader]
    if not rows:
        raise ValueError("Empty command CSV")
    if not all(math.isfinite(v) for row in rows for v in row):
        raise ValueError("Command CSV contains non-finite values")
    if any(b[0] <= a[0] for a,b in zip(rows,rows[1:])):
        raise ValueError("Command timestamps must strictly increase")
    if any(abs(v) > .4 + 1e-9 or abs(w) > 1.5 + 1e-9 for _,v,w in rows):
        raise ValueError("Commands exceed proposed MARVIN limits (0.4 m/s, 1.5 rad/s); review recording")
    return [(t-rows[0][0],v,w) for t,v,w in rows]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("csv", help="CSV produced by export_rosbag.py")
    p.add_argument("--publish-to-sim", action="store_true",
                   help="Opt in to publishing /cmd_vel on a SIM-ONLY ROS_DOMAIN_ID")
    p.add_argument("--topic", default="/cmd_vel")
    args = p.parse_args()
    commands = read_commands(args.csv)
    if not args.publish_to_sim:
        print(f"DRY RUN: {len(commands)} commands over {commands[-1][0]:.2f}s; no ROS messages sent")
        return
    domain = os.environ.get("ROS_DOMAIN_ID")
    if not domain or domain == "0":
        p.error("Set a separate nonzero ROS_DOMAIN_ID in your Gazebo-only environment first")
    if args.topic != "/cmd_vel":
        p.error("This replay intentionally publishes only /cmd_vel")
    try:
        import rclpy
        from geometry_msgs.msg import Twist
    except ImportError as exc:
        p.error(f"ROS 2 Python modules unavailable: {exc}")
    rclpy.init()
    node = rclpy.create_node("avl_sim_cmd_replay")
    pub = node.create_publisher(Twist, args.topic, 10)
    def send(v,w):
        msg=Twist()
        msg.linear.x=v
        msg.angular.z=w
        pub.publish(msg)
        rclpy.spin_once(node,timeout_sec=0.0)
    try:
        started = time.monotonic()
        for t,v,w in commands:
            time.sleep(max(0,started+t-time.monotonic()))
            send(v,w)
        # Stop the simulated rover when playback ends.
        print(f"Sent {len(commands)} commands to {args.topic}; stopping rover")
    finally:
        send(0.0,0.0)
        time.sleep(0.15)
        send(0.0,0.0)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
