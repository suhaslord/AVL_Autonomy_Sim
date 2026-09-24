# MARVIN frame contract

This file is the naming/ownership contract for MARVIN's TF tree. It does **not** contain measured mount positions; those stay in `assets/measurements.md`.

## Required tree

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

There is exactly one `base_link`.

## Frame ownership

| Parent | Child | Kind | Publisher / owner | Origin source |
|---|---|---|---|---|
| `odom` | `base_link` | dynamic | Gazebo diff-drive system | simulated motion |
| `base_link` | `velodyne` | fixed | `robot_state_publisher` | `assets/measurements.md` |
| `base_link` | `imu_link` | fixed | `robot_state_publisher` | `assets/measurements.md` |
| `base_link` | `gps_link` | fixed | `robot_state_publisher` | `assets/measurements.md` |
| `base_link` | `zed_left_link` | fixed | `robot_state_publisher` | `assets/measurements.md` |
| `base_link` | `zed_center_link` | fixed | `robot_state_publisher` | `assets/measurements.md` |
| `base_link` | `zed_right_link` | fixed | `robot_state_publisher` | `assets/measurements.md` |
| `zed_left_link` | `zed_left_optical_frame` | fixed | `robot_state_publisher` | camera optical-frame transform |
| `zed_center_link` | `zed_center_optical_frame` | fixed | `robot_state_publisher` | camera optical-frame transform |
| `zed_right_link` | `zed_right_optical_frame` | fixed | `robot_state_publisher` | camera optical-frame transform |

## Rules that keep TF sane

1. **Only the diff-drive system publishes `odom -> base_link`.**  
   The URDF / `robot_state_publisher` must not publish that edge too.

2. **All sensor mounts are children of `base_link`.**  
   Their measured `xyz` + `rpy` values come only from `assets/measurements.md`.

3. **Do not guess missing mounts.**  
   If a value is missing, the xacro uses `0 0 0` and a `TODO measure` comment.

4. **Camera optical frames are separate children of the camera links.**  
   Their optical frames point Z forward, as required by the team task list.

5. **Names are exact.**  
   Do not add alternate `base`, `base_footprint`, `lidar`, or sim-only frame aliases unless Ryan changes the contract.

## Later validation

Once `avl_description` contains the xacro, these checks should work:

```bash
ros2 launch avl_description display.launch.py
ros2 run tf2_ros tf2_echo base_link velodyne
```

For the display-only check, `use_sim_time` stays false.

Once Gazebo is running:

```bash
ros2 run tf2_ros tf2_echo odom base_link
```

Expected: one dynamic `odom -> base_link` broadcaster and fixed sensor transforms below `base_link`.
