# tests/test_environment.py
import unittest
import sys
import os
import git
import keyring

class TestEnvironment(unittest.TestCase):
    def test_python_version(self):
        self.assertTrue(sys.version_info >= (3, 10), "Python 3.10+ required")

    def test_gitpython_installed(self):
        self.assertIsNotNone(git.__version__, "GitPython not installed")
        self.assertGreaterEqual(git.__version__, "3.1.44", "GitPython version too low")

    def test_pyqt6_installed(self):
        try:
            from PyQt6.QtCore import qVersion
            self.assertTrue(callable(qVersion), "PyQt6 qVersion is not callable")
            version = qVersion()
            self.assertTrue(version.startswith("6."), "PyQt6 version must start with 6.")
            print(f"PyQt6 version: {version}")  # Debug
        except ImportError as e:
            self.fail(f"PyQt6 import failed: {e}")

    def test_keyring_installed(self):
        self.assertTrue(hasattr(keyring, 'set_password'), "Keyring not installed")
        self.assertTrue(callable(keyring.set_password), "Keyring set_password not callable")

    def test_script_runs(self):
        script_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'app_manager.py')
        result = os.system(f"python3 {script_path}")
        self.assertEqual(result, 0, "Script failed to run")

if __name__ == '__main__':
    unittest.main()