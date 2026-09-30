#pragma once

#include <chrono>
#include <cmath>
#include <cstddef>
#include <iomanip>
#include <iostream>
#include <optional>

namespace sim_chair {

struct TelemetrySample {
    double pitch_deg{};
    double yaw_deg{};
    double roll_deg{};
    double accel_x_mps2{};
    double accel_y_mps2{};
    double accel_z_mps2{};
};

class TelemetryDebugger {
public:
    explicit TelemetryDebugger(std::ostream& out = std::cout) : out_(out) {}

    bool log(const TelemetrySample& sample) {
        using clock = std::chrono::steady_clock;
        const auto now = clock::now();

        const bool finite = isFinite(sample);
        const bool angles_ok = std::abs(sample.pitch_deg) <= 180.0 &&
                               std::abs(sample.yaw_deg) <= 180.0 &&
                               std::abs(sample.roll_deg) <= 180.0;
        const bool accel_ok = std::abs(sample.accel_x_mps2) <= 200.0 &&
                              std::abs(sample.accel_y_mps2) <= 200.0 &&
                              std::abs(sample.accel_z_mps2) <= 200.0;

        double dt_ms = 0.0;
        double hz = 0.0;
        if (last_time_) {
            dt_ms = std::chrono::duration<double, std::milli>(now - *last_time_).count();
            if (dt_ms > 0.0) {
                hz = 1000.0 / dt_ms;
            }
        }

        out_ << std::fixed << std::setprecision(2)
             << "[telemetry] seq=" << sequence_
             << " dt_ms=" << dt_ms
             << " hz=" << hz
             << " pitch=" << sample.pitch_deg
             << " yaw=" << sample.yaw_deg
             << " roll=" << sample.roll_deg
             << " accel=(" << sample.accel_x_mps2 << ','
             << sample.accel_y_mps2 << ','
             << sample.accel_z_mps2 << ')';

        if (!finite) {
            out_ << " WARN=non-finite-value";
        } else if (!angles_ok) {
            out_ << " WARN=angle-out-of-range";
        } else if (!accel_ok) {
            out_ << " WARN=accel-out-of-range";
        } else if (last_time_ && dt_ms > 250.0) {
            out_ << " WARN=stale-stream";
        }

        out_ << '\n';

        last_time_ = now;
        ++sequence_;
        return finite && angles_ok && accel_ok;
    }

    std::size_t samplesSeen() const { return sequence_; }

private:
    static bool isFinite(const TelemetrySample& s) {
        return std::isfinite(s.pitch_deg) &&
               std::isfinite(s.yaw_deg) &&
               std::isfinite(s.roll_deg) &&
               std::isfinite(s.accel_x_mps2) &&
               std::isfinite(s.accel_y_mps2) &&
               std::isfinite(s.accel_z_mps2);
    }

    std::ostream& out_;
    std::optional<std::chrono::steady_clock::time_point> last_time_;
    std::size_t sequence_ = 0;
};

}  // namespace sim_chair
