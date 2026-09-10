import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'math-modeling/scripts/check_evidence.py'
spec = importlib.util.spec_from_file_location('evidence', SCRIPT)
evidence = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evidence)


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.result = self.root / 'results with spaces.json'
        self.result.write_text('{"a/b":{"~k":[0.866,1.23456]},"zero":0,"flag":true}')
        self.manifest = self.root / 'manifest.json'
        self.data = {
            'version': 1,
            'artifacts': [{'id': 'run', 'path': self.result.name,
                           'sha256': hashlib.sha256(self.result.read_bytes()).hexdigest()}],
            'claims': [{'id': 'rate', 'artifact': 'run', 'pointer': '/a~1b/~0k/0',
                        'value': 86.6, 'scale': 100, 'unit': 'percent',
                        'status': 'model_estimate', 'location': 'Summary: rate'}]}

    def save(self):
        self.manifest.write_text(json.dumps(self.data))

    def run_check(self):
        self.save()
        return evidence.check(self.manifest)

    def test_percent_conversion_and_escaped_pointer(self):
        r = self.run_check()
        self.assertEqual(r['status'], 'PASS')
        self.assertEqual(r['checks'][0]['actual_scaled'], '86.600')

    def test_wrong_metric_even_if_number_elsewhere(self):
        self.data['claims'][0]['pointer'] = '/a~1b/~0k/1'
        self.assertEqual(self.run_check()['status'], 'FAIL')

    def test_rounding_tolerance_and_boundary(self):
        c = self.data['claims'][0]
        c.update(pointer='/a~1b/~0k/1', scale=1, value=1.23, abs_tol=0.005)
        self.assertEqual(self.run_check()['status'], 'PASS')
        c['abs_tol'] = 0.004
        self.assertEqual(self.run_check()['status'], 'FAIL')

    def test_relative_tolerance_uses_source_scale(self):
        c = self.data['claims'][0]
        c.update(value=86.61, rel_tol=0.001)
        self.assertEqual(self.run_check()['status'], 'PASS')
        c['rel_tol'] = 0.00001
        self.assertEqual(self.run_check()['status'], 'FAIL')

    def test_zero_has_no_implicit_relative_tolerance(self):
        self.data['claims'][0].update(pointer='/zero', value=0.1, rel_tol=1)
        self.assertEqual(self.run_check()['status'], 'FAIL')

    def test_input_hash_detects_stale_result(self):
        self.result.write_text(self.result.read_text() + '\n')
        r = self.run_check()
        self.assertEqual(r['status'], 'FAIL')
        self.assertTrue(r['checks'][0]['matches'])

    def test_missing_and_empty_files(self):
        self.result.unlink()
        self.assertEqual(self.run_check()['status'], 'FAIL')
        self.result.write_text('')
        self.assertEqual(self.run_check()['status'], 'FAIL')

    def test_invalid_pointer_rejected(self):
        for ptr in ['/missing', '/a~1b/~0k/-1', '/a~1b/~0k/00', '/a~2b', 'zero', '/zero/x']:
            with self.subTest(ptr=ptr):
                self.data['claims'][0]['pointer'] = ptr
                with self.assertRaises(evidence.ContractError):
                    self.run_check()

    def test_boolean_source_and_numeric_string_rejected(self):
        c = self.data['claims'][0]
        c.update(pointer='/flag', value=100)
        with self.assertRaises(evidence.ContractError):
            self.run_check()
        c.update(pointer='/zero', value='0')
        with self.assertRaises(evidence.ContractError):
            self.run_check()

    def test_invalid_schema_and_tolerances(self):
        base = copy.deepcopy(self.data)
        for update in [{'scale': 0}, {'abs_tol': -1}, {'rel_tol': -1}, {'status': 'verified'}, {'abs_tlo': 1}]:
            with self.subTest(update=update):
                self.data = copy.deepcopy(base)
                self.data['claims'][0].update(update)
                with self.assertRaises(evidence.ContractError):
                    self.run_check()

    def test_duplicate_ids_and_unknown_source(self):
        base = copy.deepcopy(self.data)
        for key in ('claims', 'artifacts'):
            self.data = copy.deepcopy(base)
            self.data[key].append(copy.deepcopy(self.data[key][0]))
            with self.assertRaises(evidence.ContractError):
                self.run_check()
        self.data = copy.deepcopy(base)
        self.data['claims'][0]['artifact'] = 'missing'
        with self.assertRaises(evidence.ContractError):
            self.run_check()

    def test_empty_declarations_cannot_pass(self):
        for key in ('claims', 'artifacts'):
            old = self.data[key]
            self.data[key] = []
            with self.assertRaises(evidence.ContractError):
                self.run_check()
            self.data[key] = old

    def test_nonfinite_and_duplicate_json_keys(self):
        for raw in ['{"x":NaN}', '{"x":Infinity}', '{"x":1,"x":2}']:
            with self.assertRaises(evidence.ContractError):
                evidence.parse_json(raw)

    def test_absolute_escape_and_symlink_paths(self):
        for raw in ['/tmp/anything', '../outside']:
            self.data['artifacts'][0]['path'] = raw
            with self.assertRaises(evidence.ContractError):
                self.run_check()
        (self.root / 'linked').symlink_to(self.root.parent, target_is_directory=True)
        self.data['artifacts'][0]['path'] = 'linked/other-file'
        with self.assertRaises(evidence.ContractError):
            self.run_check()

    def test_unverified_does_not_become_verified(self):
        self.data['claims'][0]['status'] = 'unverified'
        r = self.run_check()
        self.assertEqual(r['status'], 'PASS')
        self.assertEqual(len(r['warnings']), 1)
        self.assertIn('no paper parsing', r['scope'])

    def test_cli_exit_codes_and_readonly_behavior(self):
        for value, code in [(86.6, 0), (86.7, 1), ('invalid', 2)]:
            self.data['claims'][0]['value'] = value
            self.save()
            before = (self.result.read_bytes(), self.manifest.read_bytes())
            run = subprocess.run([sys.executable, str(SCRIPT), str(self.manifest)],
                                 capture_output=True, text=True)
            self.assertEqual(run.returncode, code, run.stdout + run.stderr)
            self.assertIsInstance(json.loads(run.stdout), dict)
            self.assertEqual(before, (self.result.read_bytes(), self.manifest.read_bytes()))

    def test_bundled_example(self):
        r = evidence.check(ROOT / 'math-modeling/assets/evidence-example/manifest.json')
        self.assertEqual(r['status'], 'PASS')
        self.assertEqual(len(r['checks']), 2)
        self.assertEqual(len(r['warnings']), 2)


if __name__ == '__main__':
    unittest.main()
