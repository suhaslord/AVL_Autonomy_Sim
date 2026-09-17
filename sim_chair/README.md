# Sim chair telemetry debug helper

This directory adds a small read-only C++ helper for checking whether the sim-chair telemetry path is actually producing fresh, sane values before changing any motion-control code.

## What it logs

Each sample prints:

- sequence number
- time since the previous sample (`dt_ms`)
- estimated update rate (`hz`)
- pitch, yaw, and roll
- X/Y/Z acceleration
- warnings for non-finite values, obviously invalid ranges, or a stale stream

The helper does not send commands to the chair.

## Integration

Include `telemetry_debug.hpp` next to the existing telemetry receive/update path and pass the values already being produced by the SDK/IMU code into `TelemetryDebugger::log`.

```cpp
sim_chair::TelemetryDebugger debug;

// Inside the existing telemetry update loop:
sim_chair::TelemetrySample sample;
sample.pitch_deg = pitch;
sample.yaw_deg = yaw;
sample.roll_deg = roll;
sample.accel_x_mps2 = accel_x;
sample.accel_y_mps2 = accel_y;
sample.accel_z_mps2 = accel_z;
debug.log(sample);
```

This should make it obvious whether the current failure is upstream telemetry/struct initialization or later in the SDK motion path.

## Standalone check

The demo uses only the C++ standard library:

```bash
g++ -std=c++17 -Wall -Wextra -Wpedantic sim_chair/telemetry_debug_demo.cpp -o telemetry_debug_demo
./telemetry_debug_demo
```

On MSVC, add both files to a C++17 project and build normally.
