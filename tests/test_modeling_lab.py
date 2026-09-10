"""Numerical tests require the optional modeling-lab dependencies."""
import importlib.util
from pathlib import Path
import unittest
try:
    import numpy as np
    import scipy
except ImportError:
    np = None
if np is not None:
    spec=importlib.util.spec_from_file_location('lab',Path(__file__).resolve().parents[1]/'math-modeling/scripts/modeling_lab.py')
    lab=importlib.util.module_from_spec(spec);spec.loader.exec_module(lab)

@unittest.skipIf(np is None,'optional NumPy/SciPy not installed')
class ModelingTests(unittest.TestCase):
    def test_ahp_known_consistent_weights(self):
        w=np.array([.6,.3,.1]); got,ci,cr=lab.ahp(w[:,None]/w[None,:]);np.testing.assert_allclose(got,w);self.assertLess(ci,1e-12)
    def test_ahp_rejects_nonreciprocal(self):
        with self.assertRaises(ValueError):lab.ahp([[1,3],[.5,1]])
    def test_ahp_two_has_no_cr(self):
        self.assertIsNone(lab.ahp([[1,2],[.5,1]])[2])
    def test_topsis_direction_and_constant(self):
        np.testing.assert_allclose(lab.topsis([[1,9,3],[9,1,3]],[True,False,True],[1,1,1]),[0,1])
    def test_topsis_identical_tie(self):
        np.testing.assert_allclose(lab.topsis([[1,1],[1,1]],[True,True],[1,1]),[.5,.5])
    def test_pca_zero_sum_axis_survives(self):
        x=np.arange(5.);m=lab.pcr_fit(np.column_stack([x,-x]),4+3*x,1)
        np.testing.assert_allclose(lab.pcr_predict(m,[[8,-8]]),[28],atol=1e-12)
        self.assertAlmostEqual(np.linalg.norm(m['axes'][:,0]),1)
    def test_pcr_rank_rejected(self):
        with self.assertRaises(ValueError):lab.pcr_fit([[1,1],[2,2],[3,3]],[1,2,3],2)
    def test_gm_constant_and_initial_condition(self):
        np.testing.assert_allclose(lab.gm11([4,4,4,4],2),np.full(6,4),atol=1e-10)
        self.assertEqual(lab.gm11([2,3,4,5])[0],2)
    def test_gm_invalid_input(self):
        with self.assertRaises(ValueError):lab.gm11([1,2,0,3])
    def test_prediction_origin_no_future(self):
        self.assertEqual(lab.moving_average_next([1,2,3,4],3),3)
        y=np.array([1,2,3,4,999.]);self.assertEqual(lab.moving_average_next(y[:4],3),3)
    def test_floyd_negative_zero_and_unreachable(self):
        d=lab.floyd([[0,4,5,np.inf],[np.inf,0,-3,np.inf],[np.inf,np.inf,0,0],[np.inf,np.inf,np.inf,0]])
        self.assertEqual(d[0,2],1);self.assertEqual(d[0,3],1);self.assertTrue(np.isinf(d[3,0]))
    def test_negative_cycle_rejected(self):
        with self.assertRaises(ValueError):lab.floyd([[0,-2],[1,0]])
    def test_flow_reverse_augmentation_and_cut(self):
        c=np.zeros((6,6))
        for u,v in [(0,1),(0,2),(1,3),(1,4),(2,3),(3,5),(4,5)]:c[u,v]=1
        value,f,s=lab.max_flow(c,0,5);self.assertEqual(value,2);self.assertEqual(c[np.ix_(s,~s)].sum(),value)
        np.testing.assert_allclose(f.sum(axis=1),[2,0,0,0,0,-2]);self.assertTrue((f<=c+1e-12).all())
    def test_flow_disconnected(self):
        self.assertEqual(lab.max_flow(np.zeros((3,3)),0,2)[0],0)
    def test_sa_returns_closed_feasible_best(self):
        d=np.array([[0,1,2,1],[1,0,1,2],[2,1,0,1],[1,2,1,0]])
        tour,cost,trace=lab.anneal_tour(d,seed=2,proposals=400)
        self.assertEqual(sorted(tour),[0,1,2,3]);self.assertEqual(cost,4);self.assertEqual(cost,lab.route_cost(d,tour));self.assertTrue((np.diff(trace)<=0).all())
    def test_ca_is_synchronous_and_conservative(self):
        np.testing.assert_array_equal(lab.traffic_step([1,0,0,0]),[0,1,0,0])
        for mask in range(256):
            a=np.array([(mask>>i)&1 for i in range(8)]);b=lab.traffic_step(a)
            self.assertEqual(a.sum(),b.sum());self.assertTrue(np.isin(b,[0,1]).all())
    def test_heat_refinement_against_analytic(self):
        coarse,fine=lab.heat_error(20),lab.heat_error(40)
        self.assertGreater(coarse/fine,3.5);self.assertLess(coarse/fine,4.5)
    def test_halfpipe_frictionless_energy_and_mass_cancellation(self):
        for flat in [0,5,10]:self.assertAlmostEqual(lab.halfpipe(flat=flat,friction=0)['exit_speed'],12,places=6)
    def test_halfpipe_stopping_event(self):
        self.assertFalse(lab.halfpipe(flat=100,friction=.5,speed=1)['reached_exit'])
    def test_halfpipe_tolerance_and_friction(self):
        a=lab.halfpipe();b=lab.halfpipe(rtol=1e-11)
        self.assertLess(abs(a['exit_speed']-b['exit_speed']),1e-6);self.assertLess(a['exit_speed'],12)
    def test_suite_optimization_and_source_arithmetic(self):
        r=lab.run_suite();o=r['optimization'];self.assertAlmostEqual(o['integer_profit'],o['enumeration_profit']);self.assertGreaterEqual(o['lp_profit']+1e-8,o['integer_profit']);self.assertLess(o['max_violation'],1e-8)
        self.assertFalse(r['paper_p25']['claimed_greater_equal_holds'])
        self.assertAlmostEqual(r['paper_p25']['left_ratio'],.1796565389696169)

if __name__=='__main__':unittest.main()
