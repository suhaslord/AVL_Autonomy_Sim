# VLP-16 sim-to-real protocol

## Goal

Compare the Gazebo VLP-16 path to the real MARVIN VLP-16 on a repeatable scene without overstating what the simulator can reproduce.

## Gate before collecting results

Do not record final comparison numbers until all of these are true:

- `assets/measurements.md` has the measured VLP-16 pose relative to `base_link`.
- the Jetson inventory confirms the real point-cloud topic and frame ID;
- the Gazebo sensor publishes the same ROS 2 message type and frame convention;
- the course geometry and target distances are measured;
- the same filtering/cropping rules are used for real and simulated data.

## Course

Use the simple marker layout from `gazebo/worlds/empty_course.sdf` as the starting geometry, then replace its marker poses with measured course distances used during the real run.

Record:

- target distances and heights;
- rover starting pose;
- VLP-16 mounting pose;
- weather / major reflective-surface notes for the real run;
- sensor settings that materially affect the cloud.

## Metrics

Report at least:

1. range error on known planar/box targets;
2. points per scan / point density in matched regions;
3. dropout or missing-return fraction in matched regions;
4. frame rate / scan rate;
5. any systematic angular or mounting bias observed.

Use median plus a spread statistic where possible instead of only a single mean.

## Data handling

Keep rosbag / MCAP files out of git. Store only small derived CSV/Markdown summaries and plotting inputs in `docs/eval/results/`.

Suggested names:

```text
real_<date>_<course>.mcap
sim_<date>_<course>.mcap
summary_<date>.csv
```

## Current status

Protocol is ready, but the final sensor implementation and quantitative run are blocked on the measured MARVIN sensor pose, verified Jetson topic/frame contract, and a real reference recording.
