import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "dtc_lookup.py"


class DtcLookupRegressionTests(unittest.TestCase):
    def test_builtin_code_output_is_unchanged_shape(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--json", "P0300"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(len(payload), 1)
        entry = payload[0]
        self.assertEqual(entry["code"], "P0300")
        self.assertEqual(entry["source"], "built-in")
        self.assertEqual(entry["severity"], "high")
        self.assertIn("Random/Multiple Cylinder Misfire", entry["description"])


if __name__ == "__main__":
    unittest.main()
