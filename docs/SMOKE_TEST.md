# Gazebo closed-loop smoke test

This checks the software path only. Passing it does **not** mean the model is physically validated; the current URDF still uses clearly labeled placeholder dimensions until Ryan fills `assets/measurements.md`.

## Build

From the Docker environment:

```bash
cd /ws
colcon build --symlink-install
source /ws/install/setup.bash
```

Expected packages include:

```text
avl_sim_description
avl_gazebo_bringup
```

## Launch

```bash
ros2 launch avl_gazebo_bringup sim.launch.py
```

In a second shell:

```bash
source /ws/install/setup.bash
ros2 topic list
```

At minimum, check that `/cmd_vel`, `/odom`, `/robot_description`, `/tf`, and `/tf_static` are present.

## Manual drive

```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.3}, angular: {z: 0.2}}" -r 10
```

Then:

```bash
ros2 topic echo /odom --once
```

Pass criteria:

- MARVIN spawns without xacro/URDF errors.
- Publishing `/cmd_vel` changes the simulated pose.
- `/odom` publishes under the draft contract name.
- No ROS-side topic remap is needed for `/cmd_vel` or `/odom`.

## Important limitation

The chassis dimensions, wheel geometry, track spacing, mass confidence, and every sensor mount still need real measurements. Do not use this placeholder model for quantitative dynamics, localization accuracy, sensor alignment, or sim-to-real claims.
