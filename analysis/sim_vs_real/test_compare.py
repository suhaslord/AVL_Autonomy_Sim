import math
import tempfile
import unittest
from pathlib import Path
from compare import compare, compare_ranges, normalize, interpolate
from replay_cmd_vel import read_commands


class ComparisonTests(unittest.TestCase):
    def test_identical_motion_different_initial_pose(self):
        a=[(0,0,0,0),(1,1,0,0),(2,2,0,0)]
        b=[(2,10,-2,math.pi/2),(3,10,-1,math.pi/2),(4,10,0,math.pi/2)]
        metrics,_=compare(a,b)
        self.assertEqual(metrics['position_rmse_m'],0)
        self.assertEqual(metrics['yaw_rmse_deg'],0)

    def test_yaw_unwrap(self):
        a=normalize([(0,0,0,math.radians(179)),(1,0,0,math.radians(-179))])
        self.assertAlmostEqual(math.degrees(a[-1][3]),2,places=7)

    def test_no_extrapolation(self):
        with self.assertRaises(ValueError):
            interpolate([(0,0,0,0),(1,1,0,0)],1.1)

    def test_motion_error(self):
        a=[(0,0,0,0),(1,1,0,0)]
        b=[(0,0,0,0),(1,0.8,0,math.radians(10))]
        metrics,_=compare(a,b)
        self.assertAlmostEqual(metrics['position_final_error_m'],0.2)
        self.assertAlmostEqual(metrics['yaw_final_error_deg'],-10)

    def test_lidar_compare(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'ranges.csv'
            p.write_text('target,real_m,sim_m\ntall,3.62,3.65\n')
            result=compare_ranges(p)
            self.assertAlmostEqual(result[0]['abs_error_m'],.03)

    def test_cmd_validation(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'cmd.csv'
            p.write_text('t_s,linear_x,angular_z\n10,0.2,0\n11,0,0.1\n')
            self.assertEqual(read_commands(p)[0][0],0)
            p.write_text('t_s,linear_x,angular_z\n0,0.5,0\n')
            with self.assertRaises(ValueError):
                read_commands(p)


if __name__ == '__main__':
    unittest.main()
