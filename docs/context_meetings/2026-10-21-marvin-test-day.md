# MARVIN test day — Oct 21, 2026

Ryan's update from the sim team thread. These are **reported test notes**, not results reproduced from the bag files yet.

## What we got

- Full live topic list and tape measurements
- Two drive runs and one parked LiDAR scan
- ROS 2 bags are still on the Jetson (~1.6 GB). Copy them when the Jetson has reliable Wi-Fi, then upload to Drive.

## Measurements and topics

**Ryan owns the measurements and `topics.yaml` freeze. Do not edit those files until he says otherwise.**

Reported tape numbers:
- Track width: **0.7336 m**
- Sprocket radius: **about 0.0404 m**

Topic changes Ryan plans to freeze:
- ZED image path ends in `/rgb/color/rect/image`.
- Camera links use `zed_*_camera_link`.
- No `gps_link`; `/gnss` uses `imu_link`.
- `/rtcm` type is `mavros_msgs/msg/RTCM`.
- `/avros/wheel_debug` type is `std_msgs/msg/Float32MultiArray`.
- `/wheel_odom` runs at **20 Hz**.
- Include `/odometry/global` and `/gps/filtered`.
- On MARVIN, the EKF owns the `odom -> base_link` transform.

**Status:** These are proposed live-robot corrections; the repository's existing topic contract is *not* frozen yet.

## Work order

1. **Inventory:** Copy Ryan's Oct 19 and Oct 21 live topic results into `ros2/topic_map/INVENTORY.md` when he shares the notes. Isabella claimed this step.
2. **Measurements + topic freeze:** Ryan updates `assets/measurements.md` and `ros2/topic_map/topics.yaml`. Suhas volunteered in the thread, but Ryan's original note says he owns this step, so confirm before editing.
3. **Sim fixes — only after Ryan posts that `topics.yaml` is frozen:** Work in a separate branch.
   - Update wheel radius from `0.06985` to `0.0404` m.
   - Update track width to `0.7336` m.
   - Set max linear speed to `0.4` m/s and max angular speed to `1.5` rad/s.
   - Use `zed_*_camera_link` frames and remove `gps_link`.
4. **Sim vs real — separate branch after the freeze:**
   - Replay `drive_02`'s `/cmd_vel` in Gazebo and compare with the real run: 9 ft straight, about 6° drift left, about 410° spin.
   - Rebuild the parked scan: tall barrel 3.62 m straight ahead; small barrel 5.59 m ahead and 1.05 m right.
   - Compare simulated LiDAR ranges to the real bag. Ryan reported the real LiDAR was within about 7 mm on the tall barrel.

Claim each step in the team thread first. One branch per step. Do not begin step 3 until Ryan announces the topic freeze.

## Not done yet

- Bags have not been copied or inspected for this note.
- No sim parameters, topic files, or robot code have been changed here.
- No Gazebo replay or LiDAR comparison has been run yet.
