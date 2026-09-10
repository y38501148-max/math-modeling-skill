import copy
import gzip
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'math-modeling'

def load_module(name):
    spec = importlib.util.spec_from_file_location(name, SKILL / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

checker = load_module('check_schedule')
catalog = load_module('catalog')

class ScheduleTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((SKILL / 'assets/schedule-example.json').read_text())
    def codes(self):
        return {x['code'] for x in checker.check_schedule(self.data)['violations']}
    def test_valid_parallel_work_and_touching_intervals(self):
        self.assertTrue(checker.check_schedule(self.data)['valid'])
    def test_vehicle_overlap(self):
        self.data['operations'].append({'id':'collision','resources':['vehicle'],'start':1,'end':3})
        self.assertIn('RESOURCE_OVERLAP', self.codes())
    def test_nested_overlap_is_not_lost(self):
        self.data['operations'] = [
            {'id':'long','resources':['vehicle'],'start':0,'end':15},
            {'id':'short','resources':['vehicle'],'start':1,'end':2},
            {'id':'later','resources':['vehicle'],'start':3,'end':4}]
        result = checker.check_schedule(self.data)
        pairs = {tuple(v['operations']) for v in result['violations'] if v['code']=='RESOURCE_OVERLAP'}
        self.assertIn(('long','later'), pairs)
    def test_processing_too_short(self):
        self.data['operations'][1]['min_duration'] = 9
        self.assertIn('DURATION', self.codes())
    def test_precedence_and_transport_lag(self):
        self.data['operations'][3]['predecessors'][1]['lag'] = 6
        self.assertIn('PRECEDENCE', self.codes())
    def test_repair_period(self):
        self.data['resources']['machine']['unavailable'] = [[5,8]]
        self.assertIn('UNAVAILABLE', self.codes())
    def test_calendar_touch_is_allowed(self):
        self.data['resources']['machine']['unavailable'] = [[12,15]]
        self.assertNotIn('UNAVAILABLE', self.codes())
    def test_horizon_violation_even_with_later_deadline(self):
        self.data['horizon'] = 11
        self.data['operations'][3]['deadline'] = 20
        self.assertIn('HORIZON', self.codes())
    def test_release_and_deadline(self):
        self.data['operations'][0]['release'] = 1
        self.data['operations'][1]['deadline'] = 9
        self.assertTrue({'RELEASE','DEADLINE'} <= self.codes())
    def test_cycle(self):
        self.data['operations'][0]['predecessors'] = ['process']
        self.assertIn('PRECEDENCE_CYCLE', self.codes())
    def test_missing_predecessor(self):
        self.data['operations'][0]['predecessors'] = ['missing']
        with self.assertRaises(ValueError): checker.check_schedule(self.data)
    def test_nonfinite_numbers(self):
        for value in [float('nan'), float('inf'), True]:
            with self.subTest(value=value):
                d = copy.deepcopy(self.data); d['operations'][0]['start'] = value
                with self.assertRaises(ValueError): checker.check_schedule(d)
    def test_unknown_resource_and_duplicate_id(self):
        d = copy.deepcopy(self.data);d['operations'][0]['resources']=['unknown']
        with self.assertRaises(ValueError):checker.check_schedule(d)
        self.data['operations'][1]['id']='load'
        with self.assertRaises(ValueError):checker.check_schedule(self.data)
    def test_invalid_duration_or_empty_input(self):
        for patch in [{'operations':[]}, {'horizon':0}]:
            d = dict(self.data, **patch)
            with self.assertRaises(ValueError):checker.check_schedule(d)
        self.data['operations'][0]['end']=0
        with self.assertRaises(ValueError):checker.check_schedule(self.data)
    def test_cli_exit_codes(self):
        script=SKILL/'scripts/check_schedule.py'
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'input.json'
            for expected in [0,1,2]:
                if expected==1:self.data['operations'][0]['min_duration']=3
                if expected==2:self.data['operations'][0]['resources']=['missing']
                path.write_text(json.dumps(self.data))
                result=subprocess.run([sys.executable,str(script),str(path)],capture_output=True,text=True)
                self.assertEqual(result.returncode,expected)
                self.assertIn('valid',json.loads(result.stdout))

class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.rows=catalog.read_rows()
    def test_full_inventory_counts_and_fingerprints(self):
        self.assertEqual(len(self.rows),9893)
        self.assertEqual(len({r['blob_sha'] for r in self.rows}),7724)
        self.assertTrue(all(len(r['commit'])==40 and len(r['blob_sha'])==40 for r in self.rows))
    def test_undergraduate_filter_does_not_use_graduate_collection(self):
        found=catalog.search(self.rows,'2018 A229')
        self.assertEqual(len(found),1)
        self.assertIn('P05',found[0]['source_ids'])
        self.assertFalse(any(r['scope']=='graduate' for r in catalog.search(self.rows)))
    def test_cross_repository_blob_dedup_preserves_aliases(self):
        found=catalog.search(self.rows,'目标定位最优布局的研究.pdf',scope='all',unique=True)
        self.assertEqual(len(found),1)
        self.assertEqual({r['repo'] for r in found[0]['matching_aliases']},{'zhanwen/MathModel','personqianduixue/Math_Model'})
    def test_source_ids_resolve_to_pinned_inventory(self):
        sources=json.loads((SKILL/'references/sources.json').read_text())['sources']
        keys={(r['repo'],r['path'],r['blob_sha'],r['commit']) for r in self.rows}
        for source in sources:
            self.assertIn((source['repo'],source['path'],source['blob_sha'],source['commit']),keys)
            self.assertIn(source['commit'],source['url'])
    def test_query_is_and_matched_and_case_insensitive(self):
        self.assertEqual(catalog.search(self.rows,'2018 a229'),catalog.search(self.rows,'2018 A229'))
        self.assertEqual(catalog.search(self.rows,'2017 A229'),[])

if __name__ == '__main__':unittest.main()
