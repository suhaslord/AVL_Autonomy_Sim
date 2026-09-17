# Topic map

**Status:** draft. Names below are derived from the current `Paarseus/IGVC_ROS2` codebase; freeze only after a live Jetson graph check.

## Rules

1. Where the Jetson stack already uses a name, that name wins.
2. Gaps are added once here, then frozen with everything else.
3. No long-lived sim-only aliases unless the same name exists on the robot.
4. After freeze (`topics.yaml` -> `status: frozen`), renames need brief-owner approval.

## Files

- `topics.yaml` — machine-readable contract for bridges and launch
- `INVENTORY.md` — code-derived Jetson topic inventory + remaining live checks

## Current contract candidate

| Topic | Type | Direction from sim | Notes |
|---|---|---|---|
| `/cmd_vel` | `geometry_msgs/msg/Twist` | subscribe | Main Nav2/teleop command path |
| `/wheel_odom` | `nav_msgs/msg/Odometry` | publish | Raw simulated wheel odometry; feed the same EKF path used on MARVIN |
| `/odometry/filtered` | `nav_msgs/msg/Odometry` | publish via EKF | Canonical filtered local odometry; replaces the old `/odom` seed |
| `/imu/data` | `sensor_msgs/msg/Imu` | publish | Xsens-equivalent IMU feed |
| `/gnss` | `sensor_msgs/msg/NavSatFix` | publish | Canonical GNSS name; replaces `/gps/fix` seed |
| `/velodyne_points` | `sensor_msgs/msg/PointCloud2` | publish | VLP-16 point cloud |
| `/avros/actuator_command` | `avros_msgs/msg/ActuatorCommand` | optional subscribe | Direct-control/e-stop path; decide Phase-1 scope after live inventory |
| `/avros/actuator_state` | `avros_msgs/msg/ActuatorState` | optional publish | Actuator telemetry |

## Closed-loop architecture

Prefer parity with the real stack:

`/cmd_vel` -> Gazebo drive -> `/wheel_odom` + `/imu/data` + `/gnss` -> `robot_localization` -> `/odometry/filtered`

Do not introduce a permanent simulator-only `/odom` shortcut when the robot does not use it as the navigation contract.

## Freeze gate

Before changing `status: draft` to `status: frozen`:

1. Capture `ros2 topic list -t` on the current MARVIN Jetson.
2. Diff it against `INVENTORY.md` and `topics.yaml`.
3. Resolve any command-path differences (`/cmd_vel` vs direct `/avros/actuator_command`).
4. Confirm required ZED topics/frames for the first autonomy smoke test.
