#!/usr/bin/env python3
"""Compare measured vs Gazebo robot motion and optional LiDAR range readings.

Requires only Python 3.8+; matplotlib is optional for trajectory plots.
"""
import argparse
import csv
import json
import math
from pathlib import Path
import statistics


def read_pose(path):
    required = {"t_s", "x_m", "y_m", "yaw_rad"}
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError(f"{path}: expected columns {sorted(required)}")
        for row in reader:
            vals = tuple(float(row[k]) for k in ("t_s", "x_m", "y_m", "yaw_rad"))
            if not all(math.isfinite(v) for v in vals):
                raise ValueError(f"{path}: non-finite value")
            rows.append(vals)
    if len(rows) < 2:
        raise ValueError(f"{path}: need at least two poses")
    if any(b[0] <= a[0] for a, b in zip(rows, rows[1:])):
        raise ValueError(f"{path}: timestamps must strictly increase")
    return rows


def normalize(poses):
    """Time and heading zeroed; compare travel independent of world origin."""
    t0, x0, y0, yaw0 = poses[0]
    c, s = math.cos(yaw0), math.sin(yaw0)
    raw = [r[3] for r in poses]
    unwrapped = [raw[0]]
    for prev, current in zip(raw, raw[1:]):
        dy = (current - prev + math.pi) % (2 * math.pi) - math.pi
        unwrapped.append(unwrapped[-1] + dy)
    return [(t-t0, c*(x-x0)+s*(y-y0), -s*(x-x0)+c*(y-y0), yaw-yaw0)
            for (t,x,y,_),yaw in zip(poses, unwrapped)]


def interpolate(pose, at):
    """Linear interpolation; caller must use only times inside the trajectory."""
    lo, hi = 0, len(pose)-1
    if at < pose[0][0] or at > pose[-1][0]:
        raise ValueError("Cannot extrapolate beyond recorded data")
    while lo < hi:
        mid = (lo + hi)//2
        if pose[mid][0] < at:
            lo = mid+1
        else:
            hi = mid
    if pose[lo][0] == at:
        return pose[lo]
    left, right = pose[lo-1], pose[lo]
    w = (at - left[0])/(right[0]-left[0])
    return (at, *(left[i] + w*(right[i]-left[i]) for i in (1,2,3)))


def path_length(poses):
    return sum(math.hypot(b[1]-a[1], b[2]-a[2]) for a,b in zip(poses, poses[1:]))


def compare(real, sim):
    real, sim = normalize(real), normalize(sim)
    end = min(real[-1][0], sim[-1][0])
    times = sorted(set([0.0, end] + [p[0] for p in real if p[0] <= end] +
                       [p[0] for p in sim if p[0] <= end]))
    if end <= 0 or len(times) < 2:
        raise ValueError("No overlapping recording duration")
    pairs = [(interpolate(real, t), interpolate(sim, t)) for t in times]
    pos_err = [math.hypot(a[1]-b[1], a[2]-b[2]) for a,b in pairs]
    yaw_err = [math.degrees(a[3]-b[3]) for a,b in pairs]
    def rms(nums):
        return math.sqrt(statistics.mean(v*v for v in nums))
    real_overlap = [a for a, _ in pairs]
    sim_overlap = [b for _, b in pairs]
    return {
        "duration_compared_s": round(end, 4),
        "samples": len(pairs),
        "position_rmse_m": round(rms(pos_err), 5),
        "position_final_error_m": round(pos_err[-1], 5),
        "position_max_error_m": round(max(pos_err), 5),
        "yaw_rmse_deg": round(rms(yaw_err), 4),
        "yaw_final_error_deg": round(yaw_err[-1], 4),
        "real_path_length_m": round(path_length(real_overlap), 5),
        "sim_path_length_m": round(path_length(sim_overlap), 5),
        "real_net_displacement_m": round(math.hypot(real_overlap[-1][1], real_overlap[-1][2]), 5),
        "sim_net_displacement_m": round(math.hypot(sim_overlap[-1][1], sim_overlap[-1][2]), 5),
        "real_total_yaw_deg": round(math.degrees(real_overlap[-1][3]), 4),
        "sim_total_yaw_deg": round(math.degrees(sim_overlap[-1][3]), 4),
    }, pairs


def compare_ranges(path):
    """CSV has target, real_m, sim_m; each range must be independently measured."""
    details = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not {"target", "real_m", "sim_m"}.issubset(set(reader.fieldnames or [])):
            raise ValueError("LiDAR CSV needs target,real_m,sim_m")
        for row in reader:
            real_m, sim_m = float(row["real_m"]), float(row["sim_m"])
            if not all(math.isfinite(v) and v > 0 for v in (real_m, sim_m)):
                raise ValueError("LiDAR ranges must be positive finite meters")
            details.append({"target":row["target"], "real_m":real_m,
                            "sim_m":sim_m, "abs_error_m":round(abs(real_m-sim_m), 5)})
    if not details:
        raise ValueError("LiDAR CSV has no targets")
    return details


def plot_paths(pairs, output):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise RuntimeError("matplotlib not installed; skip --plot or install it") from exc
    a, b = [q[0] for q in pairs], [q[1] for q in pairs]
    plt.figure(figsize=(7,5))
    plt.plot([p[1] for p in a], [p[2] for p in a], label="Real MARVIN")
    plt.plot([p[1] for p in b], [p[2] for p in b], label="Gazebo")
    plt.axis("equal")
    plt.xlabel("Forward x (m) from start")
    plt.ylabel("Left y (m) from start")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output, dpi=160)
    plt.close()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--real-pose", type=Path)
    p.add_argument("--sim-pose", type=Path)
    p.add_argument("--lidar-ranges", type=Path,
                   help="Manually verified target ranges, NOT the tape distances")
    p.add_argument("--out", type=Path, default=Path("step4_metrics.json"))
    p.add_argument("--plot", type=Path)
    args = p.parse_args()
    if bool(args.real_pose) != bool(args.sim_pose):
        p.error("--real-pose and --sim-pose must be provided together")
    if not args.real_pose and not args.lidar_ranges:
        p.error("provide both pose CSVs and/or --lidar-ranges")
    result = {"notes":"real data only; no reference numbers substituted as measurements"}
    if args.real_pose:
        result["motion"], pairs = compare(read_pose(args.real_pose), read_pose(args.sim_pose))
        if args.plot:
            plot_paths(pairs, args.plot)
    elif args.plot:
        p.error("--plot requires pose CSVs")
    if args.lidar_ranges:
        result["lidar"] = compare_ranges(args.lidar_ranges)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
