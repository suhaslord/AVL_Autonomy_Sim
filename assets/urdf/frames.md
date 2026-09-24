# MARVIN frame tree

This file defines frame names and parent/child relationships only. It does **not** define measured positions.

## Tree

```text
odom
└── base_link
    ├── velodyne
    ├── imu_link
    ├── gps_link
    ├── zed_left_link
    │   └── zed_left_optical_frame
    ├── zed_center_link
    │   └── zed_center_optical_frame
    └── zed_right_link
        └── zed_right_optical_frame
```

## Rules

- `odom -> base_link` is the motion transform. The Gazebo diff-drive system owns this transform.
- `robot_state_publisher` publishes `base_link` to the fixed sensor frames only.
- There is only one `base_link`.
- Camera optical frames are fixed children of their camera links and use the ROS optical-frame convention with +Z forward.
- Sensor `xyz` / `rpy` values come only from `assets/measurements.md`.
- If a sensor mount has not been measured yet, use `0 0 0` and mark it `TODO measure` in the xacro. Do not guess a position.
