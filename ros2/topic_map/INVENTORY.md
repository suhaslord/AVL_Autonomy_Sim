# Jetson topic inventory

Source reviewed: `Paarseus/IGVC_ROS2` at commit `d40e18aa480f76673b46a379ab7cb4618f279d75`.

This is a code-derived inventory, not yet a live `ros2 topic list` capture from MARVIN. Keep `topics.yaml` in `draft` until the team verifies the live Jetson graph.

| Topic | Type | Producer / consumer | Evidence / role | Sim direction |
|---|---|---|---|---|
| `/cmd_vel` | `geometry_msgs/msg/Twist` | Nav2 / teleop -> `actuator_node` | Main velocity command path | subscribe |
| `/wheel_odom` | `nav_msgs/msg/Odometry` | `actuator_node` -> EKF | Raw wheel-derived velocity odometry used by both EKFs | publish |
| `/odometry/filtered` | `nav_msgs/msg/Odometry` | `robot_localization` EKF | Filtered local odometry consumed by navigation/diagnostics | publish via EKF |
| `/imu/data` | `sensor_msgs/msg/Imu` | Xsens MTi-680G -> EKF | 100 Hz IMU input | publish |
| `/gnss` | `sensor_msgs/msg/NavSatFix` | Xsens MTi-680G -> navsat/EKF path | Canonical GNSS topic; replaces seed `/gps/fix` | publish |
| `/velodyne_points` | `sensor_msgs/msg/PointCloud2` | Velodyne convert -> Nav2 costmaps | VLP-16 point cloud | publish |
| `/velodyne_packets` | `velodyne_msgs/msg/VelodyneScan` | Velodyne driver -> convert | Raw packet path; not required for the minimal sim contract | optional |
| `/avros/actuator_command` | `avros_msgs/msg/ActuatorCommand` | Web UI / e-stop -> `actuator_node` | Direct actuator command path | optional subscribe |
| `/avros/actuator_state` | `avros_msgs/msg/ActuatorState` | `actuator_node` -> UI/telemetry | Actuator telemetry | optional publish |
| `/nmea` | `nmea_msgs/msg/Sentence` | Xsens -> NTRIP | GPGGA feed for RTK corrections | hardware-only unless RTK is simulated |
| `/rtcm` | `mavros_msgs/msg/RTCM` | NTRIP -> Xsens | RTK correction stream | hardware-only |

## Important architecture correction

The seed map's `/odom` and `/gps/fix` names do not match the current IGVC stack. The current code uses `/wheel_odom` as the raw wheel-odometry input, `/odometry/filtered` as the local fused output, and `/gnss` for `NavSatFix`.

For Gazebo parity, the preferred path is:

`/cmd_vel` -> simulated drive -> `/wheel_odom` + simulated sensors -> existing `robot_localization` -> `/odometry/filtered`

That keeps the real Jetson localization architecture intact instead of teaching the simulator a one-off `/odom` shortcut.

## Still needs live verification before freeze

- Run `ros2 topic list -t` on the current MARVIN Jetson and compare against this file.
- Confirm whether the Gazebo closed loop should expose the direct `/avros/actuator_command` path in Phase 1 or only `/cmd_vel`.
- Confirm final ZED topics/frames needed for the first smoke test.
- Fill measured sensor mount offsets before treating TF values as final.
