# MARVIN Jetson ROS 2 topic inventory

**Status: NOT FROZEN.**

This file is the evidence sheet for Step 2.1. Ryan should only copy values into `topics.yaml` after the names/types/directions/frames/QoS are checked against the real MARVIN Jetson.

## Inventory to verify on MARVIN

| Interface | Candidate topic | Candidate type | Publisher | Subscriber(s) | Rate | QoS | Frame / child frame | Verification |
|---|---|---|---|---|---|---|---|---|
| drive command | `/cmd_vel` | `geometry_msgs/msg/Twist` | TODO Jetson | TODO Jetson | TODO Jetson | TODO Jetson | n/a | **unverified** |
| left/right RPM | no ROS topic found yet | TODO if present | TODO Jetson | TODO Jetson | TODO | TODO | n/a | **must confirm present/absent** |
| odometry | `/odom` **or another real-stack odom topic** | `nav_msgs/msg/Odometry` | TODO Jetson | TODO Jetson | TODO Jetson | TODO Jetson | `odom` -> `base_link` expected | **conflict to resolve** |
| IMU | `/imu/data` | `sensor_msgs/msg/Imu` | TODO Jetson | TODO Jetson | TODO Jetson | TODO Jetson | `imu_link` expected | **unverified** |
| GNSS | task seed: `/gps/fix`; public AVL code also uses `/gnss` | `sensor_msgs/msg/NavSatFix` | TODO Jetson | TODO Jetson | TODO Jetson | TODO Jetson | TODO Jetson | **conflict to resolve** |
| VLP-16 cloud | `/velodyne_points` | `sensor_msgs/msg/PointCloud2` | TODO Jetson | TODO Jetson | TODO Jetson | TODO Jetson | `velodyne` expected | **unverified** |
| ZED left image | TODO exact name | `sensor_msgs/msg/Image` expected | TODO Jetson | TODO Jetson | TODO | TODO | optical frame | **unverified** |
| ZED left camera info | TODO exact name | `sensor_msgs/msg/CameraInfo` expected | TODO Jetson | TODO Jetson | TODO | TODO | `zed_left_optical_frame` expected | **unverified** |
| ZED center image | TODO exact name | `sensor_msgs/msg/Image` expected | TODO Jetson | TODO Jetson | TODO | TODO | optical frame | **unverified** |
| ZED center camera info | TODO exact name | `sensor_msgs/msg/CameraInfo` expected | TODO Jetson | TODO Jetson | TODO | TODO | `zed_center_optical_frame` expected | **unverified** |
| ZED right image | TODO exact name | `sensor_msgs/msg/Image` expected | TODO Jetson | TODO Jetson | TODO | TODO | optical frame | **unverified** |
| ZED right camera info | TODO exact name | `sensor_msgs/msg/CameraInfo` expected | TODO Jetson | TODO Jetson | TODO | TODO | `zed_right_optical_frame` expected | **unverified** |
| wheel / joint state | TODO only if MARVIN publishes one | TODO | TODO Jetson | TODO Jetson | TODO | TODO | wheel joint names | **must confirm present/absent** |

## Public code cross-check — useful clues, not Jetson verification

I checked public AVL/IGVC ROS repositories so the Jetson session starts with concrete things to verify instead of a blank page. **These values are only candidates. The live MARVIN Jetson wins if anything differs.**

| Item | Public-code evidence | What to check on MARVIN |
|---|---|---|
| `/cmd_vel` | `Paarseus/IGVC_ROS2` documents `geometry_msgs/Twist` into the actuator stack; field logs show it around 20 Hz while a goal is active. | exact publishers/subscriber and QoS |
| wheel command path | the same repo shows `/cmd_vel -> actuator_node -> Teensy serial -> SparkMAX`; I found serial L/R RPM commands in firmware, but **not** separate ROS left/right RPM topics. | whether MARVIN exposes any L/R RPM ROS topic; if not, Step 6 can be skipped after freeze |
| IMU | both `Paarseus/IGVC_ROS2` and `changwemusonda/avl_slam` use `/imu/data` as `sensor_msgs/msg/Imu`; IGVC docs report 100 Hz from the Xsens. | node name, live rate, QoS, header.frame_id |
| GNSS | `Paarseus/IGVC_ROS2` uses `/gnss` as `sensor_msgs/msg/NavSatFix`, around 4 Hz in its field logs. This conflicts with the task-list seed `/gps/fix`. | **resolve `/gnss` vs `/gps/fix` on the actual Jetson** |
| VLP-16 | both public repos use `/velodyne_points` as `sensor_msgs/msg/PointCloud2`; `avl_slam` uses frame `velodyne`. | live cloud rate + QoS; public notes show different measured rates in different setups, so do not assume 10 Hz |
| odometry | `avl_slam` remaps its ICP odometry to `/odom`; `IGVC_ROS2` uses topics including `/wheel_odom` and `/odometry/filtered`. | **which odometry topic Ryan's target Jetson stack actually exposes to autonomy** |
| cameras | public AVL repos contain different camera layouts/names (front/left/right/back depending on stack), while this project contract calls for left/center/right. | enumerate the live ZED namespaces; do not copy a public repo's camera names blindly |

Public sources checked:

- `https://github.com/Paarseus/IGVC_ROS2`
- `https://github.com/changwemusonda/avl_slam`
- `https://github.com/cbmusonda/avl_lidar`

## Fast Jetson capture procedure

Run this with MARVIN's normal sensor/autonomy stack already up.

### 1. Snapshot the graph

```bash
mkdir -p /tmp/marvin_inventory

ros2 node list | sort | tee /tmp/marvin_inventory/nodes.txt
ros2 topic list -t | sort | tee /tmp/marvin_inventory/topics.txt
```

### 2. Find the likely interfaces

```bash
grep -Ei 'cmd_vel|rpm|wheel|odom|imu|gps|gnss|velodyne|zed|camera|joint' \
  /tmp/marvin_inventory/topics.txt
```

Do not force the seed name if the live graph uses a different one.

### 3. Capture publisher/subscriber + QoS

For every relevant live topic:

```bash
ros2 topic info -v <topic>
```

Copy:

- exact topic name
- exact message type
- publisher node(s)
- subscriber node(s)
- reliability
- durability
- history/depth if shown

### 4. Capture rates

Run each for several seconds:

```bash
ros2 topic hz <topic>
```

Record the measured average, not a guessed datasheet rate.

### 5. Capture frame IDs

For stamped messages:

```bash
ros2 topic echo <topic> --once --field header
```

For odometry also record:

```bash
ros2 topic echo <odom_topic> --once --field child_frame_id
```

### 6. Confirm node ownership

For every publisher/subscriber found above:

```bash
ros2 node info <node_name>
```

This is especially important when multiple nodes publish `/cmd_vel`.

## Freeze gate

Ryan can set `topics.yaml` to `status: frozen`, `version: 1` only after all of these are resolved:

- [ ] exact command topic(s)
- [ ] exact odometry topic used by autonomy
- [ ] `/imu/data` or its actual replacement
- [ ] `/gps/fix` vs `/gnss`
- [ ] VLP-16 topic, rate, frame, and QoS
- [ ] every ZED image + `camera_info` topic that is actually on MARVIN
- [ ] wheel/joint-state topic present or explicitly absent
- [ ] left/right RPM ROS topics present or explicitly absent
- [ ] publisher/subscriber node names filled in
- [ ] QoS recorded from the live graph

Until that checklist is done, this file is evidence gathering only and `topics.yaml` stays draft.
