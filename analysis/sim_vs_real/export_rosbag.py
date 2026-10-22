#!/usr/bin/env python3
"""Export /cmd_vel and odometry samples from ROS 2 bag (run in ROS Humble)."""
import argparse
import csv
from pathlib import Path


def export_bag(bag, output, odom_topic, cmd_topic):
    try:
        import rosbag2_py
        from rclpy.serialization import deserialize_message
        from rosidl_runtime_py.utilities import get_message
    except ImportError as exc:
        raise RuntimeError("Run inside the ROS 2 Humble environment (source /opt/ros/humble/setup.bash)") from exc
    reader = rosbag2_py.SequentialReader()
    storage_options = rosbag2_py.StorageOptions(uri=str(bag), storage_id="sqlite3")
    # Storage id is set by the bag's metadata; choose 'mcap' when appropriate.
    metadata = (Path(bag)/"metadata.yaml").read_text(encoding="utf-8")
    if "storage_identifier: mcap" in metadata:
        storage_options = rosbag2_py.StorageOptions(uri=str(bag), storage_id="mcap")
    reader.open(storage_options, rosbag2_py.ConverterOptions("", ""))
    declared = {t.name:t.type for t in reader.get_all_topics_and_types()}
    if cmd_topic not in declared:
        raise ValueError(f"{cmd_topic} missing. Available: {sorted(declared)}")
    for name, expected in [(cmd_topic,"geometry_msgs/msg/Twist"),
                           (odom_topic,"nav_msgs/msg/Odometry")]:
        if name in declared and declared[name] != expected:
            raise ValueError(f"{name} has unexpected type {declared[name]}")
    output.mkdir(parents=True, exist_ok=True)
    csv_cmd = (output/"cmd_vel.csv").open("w",newline="",encoding="utf-8")
    csv_odom = (output/"pose.csv").open("w",newline="",encoding="utf-8")
    try:
        w_cmd = csv.writer(csv_cmd)
        w_pose = csv.writer(csv_odom)
        w_cmd.writerow(["t_s","linear_x","angular_z"])
        w_pose.writerow(["t_s","x_m","y_m","yaw_rad"])
        first_ns = None
        counts = {cmd_topic:0, odom_topic:0}
        msg_types = {k:get_message(declared[k]) for k in (cmd_topic,odom_topic) if k in declared}
        while reader.has_next():
            topic, raw, ns = reader.read_next()
            if topic not in msg_types:
                continue
            if first_ns is None:
                first_ns = ns
            msg = deserialize_message(raw,msg_types[topic])
            t = (ns-first_ns)*1e-9
            if topic == cmd_topic:
                w_cmd.writerow([f"{t:.9f}",msg.linear.x,msg.angular.z])
            else:
                q=msg.pose.pose.orientation
                import math
                yaw=math.atan2(2*(q.w*q.z + q.x*q.y), 1-2*(q.y*q.y+q.z*q.z))
                p=msg.pose.pose.position
                w_pose.writerow([f"{t:.9f}",p.x,p.y,yaw])
            counts[topic] += 1
    finally:
        csv_cmd.close()
        csv_odom.close()
    if counts[cmd_topic] == 0:
        raise ValueError("No command samples in bag")
    print(f"Exported {counts}. Files: {output}/cmd_vel.csv and pose.csv")
    if counts[odom_topic] == 0:
        print("No odometry samples. Use another --odom-topic or record a pose topic during replay.")


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("bag",type=Path,help="ROS 2 bag directory containing metadata.yaml")
    p.add_argument("--out",type=Path,default=Path("exported"))
    p.add_argument("--odom-topic",default="/odometry/filtered")
    p.add_argument("--cmd-topic",default="/cmd_vel")
    args=p.parse_args()
    export_bag(args.bag,args.out,args.odom_topic,args.cmd_topic)


if __name__ == "__main__":
    main()
