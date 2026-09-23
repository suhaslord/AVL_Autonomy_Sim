# Sensor and autonomy integration path

This is the working map for how MARVIN data should flow through the simulator. Exact ROS 2 names stay provisional until the Jetson inventory is verified.

## Closed-loop path

```text
Autonomy
  |
  | /cmd_vel (seed name; verify on Jetson)
  v
ROS 2 / ros_gz bridge
  |
  v
Gazebo skid-steer drive
  |
  +--> simulated odometry --> bridge --> /odom --> autonomy/localization
  |
  +--> simulated IMU ------> bridge --> /imu/data --> localization
  |
  +--> simulated GNSS -----> bridge --> /gps/fix --> localization
  |
  +--> simulated VLP-16 ---> bridge --> /velodyne_points --> perception
  |
  +--> simulated ZED X ----> bridge --> camera topics TBD --> perception
```

## Hardware-to-sim mapping

| Real MARVIN hardware | Sim responsibility | ROS 2 contract |
|----------------------|-------------------|----------------|
| Velodyne VLP-16 | Gazebo lidar attached to measured `velodyne` frame | `/velodyne_points` seed; verify |
| 3× Stereolabs ZED X | Camera sensors at measured left/center/right mounts | exact image/camera_info names TBD |
| Xsens MTi-680G | IMU + GNSS outputs at measured frames | `/imu/data`, `/gps/fix` seeds; verify |
| Track encoders / drivetrain | skid-steer proxy + odometry | `/odom` seed; verify |
| Jetson autonomy | same nodes should run without sim-only remaps | consumes sensor topics, publishes command topic |

## What can be built now

- Docker/ROS 2/Gazebo environment
- topic-inventory scaffold
- bridge/launch structure once the real topic names are known
- tests around topic-contract loading and command handling that do not require physical dimensions

## Current blockers

1. `assets/measurements.md` still has no chassis, track, or sensor-mount measurements.
2. The MARVIN URDF/meshes are not in `assets/` yet.
3. `gazebo/` has no rover model/world yet, so there is no project simulation to launch.
4. The Jetson inventory is not verified, so `topics.yaml` must stay draft.
5. Exact ZED and possible Teensy L/R RPM interfaces are still unknown.

Until those are resolved, placeholder geometry is okay only when clearly marked `TODO measure`; topic names should not be frozen or guessed.
