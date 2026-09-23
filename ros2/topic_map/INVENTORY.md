# Jetson ROS 2 inventory

**Status:** collection scaffold only. Nothing in this file is frozen yet.

The seed rows below come from the project abstract/topic-map draft. Replace or confirm them from the real Jetson before `topics.yaml` becomes `status: frozen`.

| Node | Topic | Type | Pub/Sub on Jetson | Owner/package | Verified source | Status |
|------|-------|------|-------------------|---------------|-----------------|--------|
| unknown | `/cmd_vel` | `geometry_msgs/msg/Twist` | unknown | unknown | project seed | unverified |
| unknown | `/odom` | `nav_msgs/msg/Odometry` | unknown | unknown | project seed | unverified |
| unknown | `/imu/data` | `sensor_msgs/msg/Imu` | unknown | Xsens path TBD | project seed | unverified |
| unknown | `/gps/fix` | `sensor_msgs/msg/NavSatFix` | unknown | Xsens/GNSS path TBD | project seed | unverified |
| unknown | `/velodyne_points` | `sensor_msgs/msg/PointCloud2` | unknown | VLP-16 path TBD | project seed | unverified |
| unknown | unknown ZED topics | image / camera_info TBD | unknown | ZED X path TBD | hardware list only | unverified |
| unknown | unknown L/R RPM topics | type TBD | unknown | Teensy/drive path TBD | design note only | unverified |

## Collect on the Jetson

Run these on the real robot or against a representative bag/session:

```bash
ros2 node list
ros2 topic list -t
```

Then inspect each relevant node:

```bash
ros2 node info <node_name>
```

For each command, odometry, IMU, GNSS, LiDAR, camera, and track-control topic, record the exact node, exact topic name, message type, and whether the Jetson publishes or subscribes.

## Freeze gate

Do **not** set `topics.yaml` to `frozen` until:

- command and odometry paths are confirmed;
- VLP-16, Xsens/GNSS, and ZED names/types are confirmed or explicitly deferred;
- any Teensy-style left/right RPM interface is confirmed or removed;
- conflicts are resolved in favor of the real Jetson interface.
