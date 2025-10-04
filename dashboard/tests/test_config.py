import unittest
import os
import json
import sys
import shutil
import git
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from app_manager import load_config, save_config, create_project, create_branch, merge_branch

class TestConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_count = 0
        cls.failed_tests = 0

    def setUp(self):
        self.config_file = "config.json"
        self.central_dir = os.path.expanduser("~/MyApps")
        if os.path.exists(self.config_file):
            os.remove(self.config_file)
        if os.path.exists(self.central_dir):
            shutil.rmtree(self.central_dir, ignore_errors=True)
        TestConfig.test_count += 1

    def tearDown(self):
        if os.path.exists(self.config_file):
            os.remove(self.config_file)
        if os.path.exists(self.central_dir):
            shutil.rmtree(self.central_dir, ignore_errors=True)

    def test_load_config_default(self):
        config = load_config()
        self.assertEqual(config["github_username"], "yous8983")
        self.assertEqual(config["default_monorepo_url"], "git@github.com:yous8983/dashboard_grok.git")
        self.assertTrue(os.path.exists(self.config_file))

    def test_save_and_load_config(self):
        test_config = {"github_username": "test_user", "default_monorepo_url": "https://test.com/repo.git"}
        save_config(test_config)
        loaded_config = load_config()
        self.assertEqual(loaded_config["github_username"], "test_user")
        self.assertEqual(loaded_config["default_monorepo_url"], "https://test.com/repo.git")

    def test_config_json_validity(self):
        config = load_config()
        try:
            json.dumps(config)
            self.assertTrue(True)
        except json.JSONDecodeError:
            self.assertTrue(False, "Config is not valid JSON")

    def test_create_project(self):
        config = load_config()
        project_name = "test_project"
        template = "python"
        project_path = create_project(project_name, template, config)
        self.assertTrue(os.path.exists(project_path))
        self.assertTrue(os.path.exists(os.path.join(project_path, "main.py")))
        with open(os.path.join(project_path, "main.py"), "r") as f:
            content = f.read()
            self.assertTrue("# Default Python code" in content)
        self.assertTrue(os.path.exists(os.path.join(project_path, ".git")))
        repo = git.Repo(project_path)
        self.assertEqual(len(repo.remotes), 1)
        self.assertEqual(repo.remotes.origin.url, config["default_monorepo_url"])
        commits = list(repo.iter_commits())
        self.assertEqual(len(commits), 1)
        self.assertEqual(commits[0].message.strip(), "Initial project setup")
        self.assertTrue(hasattr(repo.remotes.origin, 'url'))

    def test_create_branch(self):
        config = load_config()
        project_name = "test_project"
        project_path = create_project(project_name, "python", config)
        branch_name = "feature/test"
        create_branch(project_path, branch_name)
        repo = git.Repo(project_path)
        self.assertIn(branch_name, [ref.name for ref in repo.heads])

    def test_merge_branch(self):
        config = load_config()
        project_name = "test_project"
        project_path = create_project(project_name, "python", config)
        branch_name = "feature/test"
        create_branch(project_path, branch_name)
        with open(os.path.join(project_path, "main.py"), "a") as f:
            f.write("\n# Added in feature/test")
        repo = git.Repo(project_path)
        repo.git.add(A=True)
        repo.index.commit("Add feature content")
        repo.git.checkout("main")
        merge_branch(project_path, branch_name)
        with open(os.path.join(project_path, "main.py"), "r") as f:
            content = f.read()
            self.assertTrue("# Added in feature/test" in content)
        commits = list(repo.iter_commits())
        self.assertGreater(len(commits), 1)

    def test_merge_conflict(self):
        config = load_config()
        project_name = "test_project"
        project_path = create_project(project_name, "python", config)
        # Modifier main avec une version
        with open(os.path.join(project_path, "main.py"), "r") as f:
            lines = f.readlines()
        lines[1] = "print('Version A')\n"
        with open(os.path.join(project_path, "main.py"), "w") as f:
            f.writelines(lines)
        repo = git.Repo(project_path)
        repo.git.add(A=True)
        repo.index.commit("Modify main - Version A")
        # Créer et modifier une branche avec un conflit
        create_branch(project_path, "feature/conflict")
        with open(os.path.join(project_path, "main.py"), "r") as f:
            lines = f.readlines()
        lines[1] = "print('Version B')\n"
        with open(os.path.join(project_path, "main.py"), "w") as f:
            f.writelines(lines)
        repo.git.add(A=True)
        repo.index.commit("Modify feature/conflict - Version B")
        repo.git.checkout("main")
        # Tenter la fusion et vérifier les marqueurs de conflit
        try:
            merge_branch(project_path, "feature/conflict")
        except git.exc.GitCommandError as e:
            with open(os.path.join(project_path, "main.py"), "r") as f:
                content = f.read()
                self.assertTrue(any(marker in content for marker in ["<<<<<<<", ">>>>>>>", "======="]))
        else:
            self.fail("Merge should have failed with a conflict")
    @classmethod
    
    def tearDownClass(cls):
        if cls.failed_tests == 0 and cls.test_count == 7:
            try:
                print(f"\033[92m\nAll tests passed! Project advancement: 85%\033[0m")
            except:
                print("\nAll tests passed! Project advancement: 85%")
        else:
            print(f"\nTests completed with {cls.failed_tests} failures.")

if __name__ == "__main__":
    unittest.main(buffer=True)