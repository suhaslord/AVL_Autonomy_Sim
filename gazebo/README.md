# Gazebo

The current software bootstrap contains:

- `worlds/empty_course.sdf` — minimal Fortress world with repeatable landmarks;
- the skid-steer system plugin inside `ros2/avl_sim_description/urdf/tracked_rover.urdf.xacro`;
- `ros2/avl_gazebo_bringup` — launch + ROS/Gazebo bridge.

The model is intentionally a **placeholder**, not a measured digital twin yet.

Before validation, replace the placeholder geometry and every zero sensor mount from `assets/measurements.md`, then verify the Jetson topic map. VLP-16, ZED X, Xsens/GNSS simulation should be added only against that measured/frozen interface.
