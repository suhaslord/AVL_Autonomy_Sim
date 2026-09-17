#include "telemetry_debug.hpp"

#include <chrono>
#include <thread>

int main() {
    sim_chair::TelemetryDebugger debug;

    for (int i = 0; i < 5; ++i) {
        sim_chair::TelemetrySample sample;
        sample.pitch_deg = 0.5 * i;
        sample.yaw_deg = -0.25 * i;
        sample.roll_deg = 0.0;
        sample.accel_x_mps2 = 0.02 * i;
        sample.accel_y_mps2 = 0.0;
        sample.accel_z_mps2 = 9.81;

        if (!debug.log(sample)) {
            return 1;
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(16));
    }

    return 0;
}
