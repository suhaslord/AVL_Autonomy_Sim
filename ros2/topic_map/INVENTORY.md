# Jetson ROS 2 topic inventory

**Status:** in progress — do not freeze `topics.yaml` from this file yet.

This is the collection sheet for the real MARVIN Jetson. The names below are the topics the task list says to look for. A row is not considered verified until it is checked on the Jetson or from the exact package running on MARVIN.

| Topic / interface | Expected type | Publisher on Jetson | Subscriber on Jetson | Rate | QoS | Frame ID | Status |
|---|---|---|---|---|---|---|---|
| `/cmd_vel` | `geometry_msgs/msg/Twist` | TODO verify | TODO verify | TODO | TODO | n/a | required check |
| left/right RPM | TODO only if Teensy actually exposes it | TODO verify | TODO verify | TODO | TODO | n/a | verify whether it exists |
| `/odom` | `nav_msgs/msg/Odometry` | TODO verify | TODO verify | TODO | TODO | `odom` / child `base_link` expected | required check |
| `/imu/data` | `sensor_msgs/msg/Imu` | TODO verify | TODO verify | TODO | TODO | `imu_link` expected | required check |
| `/gps/fix` | `sensor_msgs/msg/NavSatFix` | TODO verify | TODO verify | TODO | TODO | TODO verify | required check |
| `/velodyne_points` | `sensor_msgs/msg/PointCloud2` | TODO verify | TODO verify | TODO | TODO | `velodyne` expected | required check |
| ZED left image | TODO verify exact topic/type | TODO verify | TODO verify | TODO | TODO | optical frame | required check |
| ZED left camera_info | `sensor_msgs/msg/CameraInfo` expected | TODO verify | TODO verify | TODO | TODO | `zed_left_optical_frame` expected | required check |
| ZED center image | TODO verify exact topic/type | TODO verify | TODO verify | TODO | TODO | optical frame | required check |
| ZED center camera_info | `sensor_msgs/msg/CameraInfo` expected | TODO verify | TODO verify | TODO | TODO | `zed_center_optical_frame` expected | required check |
| ZED right image | TODO verify exact topic/type | TODO verify | TODO verify | TODO | TODO | optical frame | required check |
| ZED right camera_info | `sensor_msgs/msg/CameraInfo` expected | TODO verify | TODO verify | TODO | TODO | `zed_right_optical_frame` expected | required check |
| wheel / joint state | TODO only if real robot publishes it | TODO verify | TODO verify | TODO | TODO | TODO verify | verify whether it exists |

## Jetson collection commands

Run on the real MARVIN Jetson with the normal autonomy/sensor stack running:

```bash
ros2 node list
ros2 topic list -t
```

For each relevant topic:

```bash
ros2 topic info -v <topic>
ros2 topic hz <topic>
```

For each publisher/subscriber node:

```bash
ros2 node info <node_name>
```

Also record QoS from `ros2 topic info -v`. Do not infer reliable vs best-effort.

## Freeze checklist

Before Ryan copies this into `topics.yaml`:

- exact topic names are verified on MARVIN;
- message types are verified;
- publisher and subscriber node names are filled in;
- rate is recorded where available;
- QoS is recorded;
- frame IDs are checked from real messages;
- left/right RPM is either confirmed or explicitly marked absent;
- wheel/joint-state output is either confirmed or explicitly marked absent.
