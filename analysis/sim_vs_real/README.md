# Step 4: MARVIN sim vs real

Prepared from Ryan's Oct 21 test-day notes. **No real ROS bag or Gazebo comparison has been run yet.** These scripts can be used after the bags arrive and Ryan freezes the topic contract.

## Reference observations, not sim results

- Drive 02: 9 ft straight (about 2.743 m), about 6 degrees drift left, about 410 degrees in the spin.
- Parked scan: tall barrel 3.62 m ahead; small barrel 5.59 m forward and 1.05 m right.
- Ryan said the **real** LiDAR was within about 7 mm of the tall-barrel tape measurement. This is **not** a sim-vs-real error.
- Tape distances and LiDAR ranges are different measurements. Only compare corresponding real/sim LiDAR ranges in matching coordinate frames.

## Scripts

1. export_rosbag.py: extract timestamped /cmd_vel and odometry data into CSV from a ROS 2 Humble bag.
2. replay_cmd_vel.py: review the command sequence (dry-run by default) or replay to a simulation-only ROS domain.
3. compare.py: compare two pose trajectories, calculate position/yaw errors and optional LiDAR-range errors; optionally save a plot.
4. test_compare.py: six offline tests. None require Gazebo or bag data.

## Run

From the repository root, run the offline tests:

    python3 -m unittest discover -s analysis/sim_vs_real -p 'test_*.py'

For bag export, use Ubuntu with ROS 2 Humble sourced. The bag folder should contain metadata.yaml.

    python3 analysis/sim_vs_real/export_rosbag.py path/to/drive_02 --out /tmp/real_02 --odom-topic /odometry/filtered

Dry run (no commands sent):

    python3 analysis/sim_vs_real/replay_cmd_vel.py /tmp/real_02/cmd_vel.csv

Only after the topic freeze and sim changes, launch Gazebo on its **own isolated** ROS_DOMAIN_ID (do not connect the physical Jetson to that domain). In that environment, replay with explicit opt-in:

    export ROS_DOMAIN_ID=67
    python3 analysis/sim_vs_real/replay_cmd_vel.py /tmp/real_02/cmd_vel.csv --publish-to-sim

Capture the simulated odometry, export to pose.csv, and compare the two runs:

    python3 analysis/sim_vs_real/compare.py --real-pose /tmp/real_02/pose.csv --sim-pose /tmp/sim_02/pose.csv --out /tmp/step4_metrics.json --plot /tmp/step4_paths.png

**Important:** Trim the real and sim pose CSVs to equivalent run start events before comparing; the tool zeroes each trajectory at its first pose and interpolates over the shared time interval. A sim recording that starts before replay will otherwise yield misleading errors.

Pose CSV header: t_s,x_m,y_m,yaw_rad
Command CSV header: t_s,linear_x,angular_z

For LiDAR, extract the range to each barrel from the actual real and sim sensor point clouds (with matching coordinate frames). Save a separate CSV:

    target,real_m,sim_m
    tall_barrel,REPLACE_WITH_REAL_RANGE,REPLACE_WITH_SIM_RANGE
    small_barrel,REPLACE_WITH_REAL_RANGE,REPLACE_WITH_SIM_RANGE

Then run:

    python3 analysis/sim_vs_real/compare.py --lidar-ranges /tmp/barrel_ranges.csv --out /tmp/lidar_metrics.json

The scripts never use the tape/reference distances as fake sensor data.

## Still needed

- Real ROS bag files for drive_02 and the parked LiDAR scan.
- Ryan's topic freeze and step 3 sim corrections.
- Gazebo odometry and simulated LiDAR output (not yet wired in the original repo).
- Actual metrics, plots, and repeatable sim-vs-real test results.

Keep this on its own step 4 branch; do not modify Ryan's measurements, topic contract, or the step 3 simulator files.
