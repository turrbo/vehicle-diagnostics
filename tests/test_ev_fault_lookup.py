import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "ev_fault_lookup.py"


class EvFaultLookupCLITests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_search_keyword_returns_tesla_charge_family_as_json(self):
        result = self.run_cli("--json", "search", "charge")
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = json.loads(result.stdout)

        self.assertTrue(any(item["oem"] == "tesla" for item in payload))
        self.assertTrue(any(item["system"] == "charge" for item in payload))

    def test_oem_lookup_matches_family_prefix(self):
        result = self.run_cli("--json", "oem", "toyota", "P0A80")
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = json.loads(result.stdout)

        self.assertEqual(payload["oem"], "toyota")
        self.assertEqual(payload["system"], "hv_battery")
        self.assertIn("replace hybrid battery pack", payload["meaning"].lower())

    def test_system_filter_returns_only_requested_branch(self):
        result = self.run_cli("--json", "system", "thermal")
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = json.loads(result.stdout)

        self.assertGreaterEqual(len(payload), 1)
        self.assertTrue(all(item["system"] == "thermal" for item in payload))

    def test_inverter_branch_has_curated_families(self):
        result = self.run_cli("--json", "system", "inverter")
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = json.loads(result.stdout)

        self.assertGreaterEqual(len(payload), 1)
        self.assertTrue(all(item["system"] == "inverter" for item in payload))

    def test_unknown_oem_code_returns_nonzero_exit(self):
        result = self.run_cli("oem", "ford", "P1ABC")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("No EV fault family match", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
