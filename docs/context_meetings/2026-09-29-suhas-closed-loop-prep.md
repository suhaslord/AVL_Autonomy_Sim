# Suhas closed-loop prep

Personal prep note before the next lab check. This does not freeze any new names or measurements.

## what already works

- rover spawns in Fortress
- diff-drive plugin is in the xacro
- /cmd_vel is the ROS command name
- current launch relays /cmd_vel -> /model/tracked_rover/cmd_vel and bridges that into Gazebo
- frames + IGVC-based topic inventory are already in main
- zed_center_link stays as the URDF frame for now even though the IGVC namespace is zed_front

## what is still missing for the real closed loop

- /clock bridged back to ROS
- Gazebo odometry bridged back to ROS
- confirm whether the sim should expose raw odom as /wheel_odom only, then let the normal EKF produce /odometry/filtered
- confirm the live Jetson names before changing any topic/frame names
- confirm the final odom -> base_link broadcaster so there is only one
- no made-up sensor mounts or dimensions

## Wednesday live checks

With MARVIN's normal stack running:

```bash
ros2 node list
ros2 topic list -t
```

For the important interfaces:

```bash
ros2 topic info -v /cmd_vel
ros2 topic info -v /wheel_odom
ros2 topic info -v /odometry/filtered
ros2 topic info -v /imu/data
ros2 topic info -v /gnss
ros2 topic info -v /velodyne_points
```

Check rates where they are actually publishing:

```bash
ros2 topic hz /wheel_odom
ros2 topic hz /odometry/filtered
ros2 topic hz /imu/data
ros2 topic hz /velodyne_points
```

Check odom/frame details:

```bash
ros2 topic echo /wheel_odom --once --field child_frame_id
ros2 topic echo /odometry/filtered --once --field child_frame_id
ros2 topic echo /imu/data --once --field header
ros2 topic echo /velodyne_points --once --field header
```

Also check the front ZED namespace/path on the live robot before renaming anything.

## after Ryan confirms the live setup

1. update INVENTORY.md only where the live Jetson differs
2. make Gazebo publish the confirmed raw odom topic
3. bridge /clock + confirmed odom back to ROS
4. verify use_sim_time
5. drive with /cmd_vel
6. echo odom and check TF odom -> base_link
7. only then clean up the temporary command relay if the final Gazebo topic can be set directly

Pass condition: /cmd_vel moves the rover, ROS receives the expected odometry topic, sim time is active, and there is one odom -> base_link publisher.
