import os
import json
import git
import sys
import logging

# Constants
CONFIG_FILE = "config.json"
LOG_FILE = "app_manager.log"

# Setup logger
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Config Functions
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            # Migration : Ajoute username et password s'ils manquent
            if "username" not in config:
                config["username"] = "admin"
                logging.info("Migrated 'username' to config.")
            if "password" not in config:
                config["password"] = "admin123"
                logging.info("Migrated 'password' to config.")
            save_config(config)  # Sauvegarde systématiquement après migration
            logging.info("Config loaded and migrated successfully.")
            return config
    else:
        default_config = {
            "username": "admin",
            "password": "admin123",
            "github_username": "yous8983",
            "default_monorepo_url": "git@github.com:yous8983/dashboard_grok.git",
            "central_directory": os.path.expanduser("~/MyApps"),
            "templates": {
                "python": {"files": {"main.py": "# Default Python code\nprint('Hello World')\n"}},
                "web": {"files": {"index.html": "<html><body><h1>Hello</h1></body></html>"}},
                "empty": {"files": {}}
            }
        }
        save_config(default_config)
        logging.info("Default config created.")
        return default_config

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
    logging.info("Config updated.")

# Auth Function
def authenticate(username, password):
    config = load_config()
    return config.get("username") == username and config.get("password") == password

# Project Functions
def create_project(name, template, config, link_remote=True, init_git=True):
    central_dir = config["central_directory"]
    os.makedirs(central_dir, exist_ok=True)
    project_path = os.path.join(central_dir, name)
    print(f"Creating project at: {project_path}")
    os.makedirs(project_path, exist_ok=True)
    
    template_files = config["templates"].get(template, {"files": {}})["files"]
    for file_name, content in template_files.items():
        file_path = os.path.join(project_path, file_name)
        print(f"Writing file: {file_path}")
        with open(file_path, "w") as f:
            f.write(content)
    
    if init_git:
        repo = git.Repo.init(project_path)
        commit_changes(project_path, "Initial project setup", config)
        if "main" not in [branch.name for branch in repo.heads]:
            repo.git.checkout("-b", "main")
        if link_remote:
            link_to_remote(project_path, config)
    return project_path

def commit_changes(project_path, message, config):
    repo = git.Repo(project_path)
    repo.git.add(A=True)
    repo.index.commit(message)

def link_to_remote(project_path, config):
    repo = git.Repo(project_path)
    remote_url = config["default_monorepo_url"]
    if not any(remote.name == "origin" for remote in repo.remotes):
        repo.create_remote("origin", remote_url)
    try:
        repo.git.branch("--set-upstream-to", "origin/main")
    except git.exc.GitCommandError as e:
        logging.error(f"Error linking to remote: {e}")
        print(f"Error linking to remote: {e}")

def push_changes(project_path, config):
    repo = git.Repo(project_path)
    try:
        # Vérifie les changements et les ajoute
        status = repo.git.status("--porcelain")
        if status:
            repo.git.add(A=True)
            commit_message = f"Automatic commit from dashboard at {os.path.basename(project_path)}"
            repo.index.commit(commit_message)
            logging.info(f"Committed changes automatically for {project_path}")
            print(f"Committed changes automatically with message: {commit_message}")
        # Exécute le push
        repo.git.push("--set-upstream", "origin", "main")
        logging.info(f"Push to remote completed successfully for {project_path}")
        print("Push to remote completed successfully.")
    except git.exc.GitCommandError as e:
        logging.error(f"Error during push for {project_path}: {e}")
        print(f"Error during push: {e}. Ensure the remote repository exists and authentication is configured.")
        raise

def pull_changes(project_path, config):
    repo = git.Repo(project_path)
    try:
        repo.git.pull("origin", "main")
        logging.info(f"Pull from remote completed successfully for {project_path}")
        print("Pull from remote completed successfully.")
    except git.exc.GitCommandError as e:
        logging.error(f"Error during pull for {project_path}: {e}")
        if "CONFLICT" in str(e):
            print("Merge conflict detected. Resolving interactively...")
            resolve_merge_conflict_interactive(project_path)
        else:
            print(f"Error during pull: {e}. Ensure the remote repository exists and authentication is configured.")
        raise

def create_branch(project_path, branch_name):
    repo = git.Repo(project_path)
    try:
        repo.git.checkout("-b", branch_name)
        logging.info(f"Branch '{branch_name}' created successfully for {project_path}")
        print(f"Branch '{branch_name}' created successfully.")
    except git.exc.GitCommandError as e:
        logging.error(f"Error creating branch '{branch_name}' for {project_path}: {e}")
        print(f"Error creating branch '{branch_name}': {e}")

def merge_branch(project_path, branch_name):
    repo = git.Repo(project_path)
    try:
        repo.git.checkout("main")
        result = repo.git.merge("--no-commit", branch_name)
        if any(".merge" in f.path for f in repo.untracked_files):
            raise git.exc.GitCommandError("Merge failed", 1, "Merge conflict detected")
        logging.info(f"Branch '{branch_name}' merged into 'main' successfully for {project_path}")
        print(f"Branch '{branch_name}' merged into 'main' successfully.")
        repo.git.merge("--continue")
        return True
    except git.exc.GitCommandError as e:
        logging.error(f"Error merging branch '{branch_name}' for {project_path}: {e}")
        if "CONFLICT" in str(e) or any(".merge" in f.path for f in repo.untracked_files):
            print(f"Warning: Merge conflict detected in branch '{branch_name}'. Resolve manually.")
            return False
        else:
            print(f"Error merging branch '{branch_name}': {e}")
            return False

def resolve_merge_conflict_interactive(project_path):
    repo = git.Repo(project_path)
    if any(".merge" in f.path for f in repo.untracked_files):
        print("Merge conflicts detected. Conflicted files:")
        for f in repo.untracked_files:
            if ".merge" in f.path:
                print(f"- {f.path}")
        print("Resolve conflicts manually, then:")
        print("- Press Enter to continue and commit, or 'q' to quit.")
        while True:
            user_input = input("> ").strip()
            if user_input == 'q':
                logging.info("Conflict resolution aborted for {project_path}")
                print("Conflict resolution aborted.")
                return False
            elif user_input == '':
                if not any(".merge" in f.path for f in repo.untracked_files):
                    commit_changes(project_path, "Resolved merge conflicts", {})
                    logging.info("Conflicts resolved and committed for {project_path}")
                    print("Conflicts resolved and committed.")
                    return True
                else:
                    print("Conflicts still present. Resolve them and try again.")
    return True

def list_projects(config):
    central_dir = config["central_directory"]
    if os.path.exists(central_dir):
        projects = [d for d in os.listdir(central_dir) if os.path.isdir(os.path.join(central_dir, d))]
        logging.info(f"Listed projects: {projects}")
        print("Existing projects:", projects)
    else:
        logging.warning("No projects found. Central directory does not exist.")
        print("No projects found. Central directory does not exist.")

def delete_project(project_name, config):
    project_path = os.path.join(config["central_directory"], project_name)
    if os.path.exists(project_path):
        import shutil
        shutil.rmtree(project_path)
        logging.info(f"Project '{project_name}' deleted successfully.")
        print(f"Project '{project_name}' deleted successfully.")
    else:
        logging.warning(f"Project '{project_name}' not found.")
        print(f"Project '{project_name}' not found.")

def list_commits(project_path):
    if not os.path.exists(project_path):
        logging.error(f"Project path '{project_path}' does not exist.")
        print(f"Error: Project path '{project_path}' does not exist.")
        return []
    try:
        repo = git.Repo(project_path)
        commits = list(repo.iter_commits())
        if not commits:
            logging.info(f"No commits found in {project_path}")
            print("No commits found in this project.")
            return []
        logging.info(f"Listed {len(commits)} commits for {project_path}")
        return commits
    except git.exc.InvalidGitRepositoryError:
        logging.error(f"Error: '{project_path}' is not a valid Git repository.")
        print(f"Error: '{project_path}' is not a valid Git repository.")
        return []

def status(project_path):
    if not os.path.exists(project_path):
        logging.error(f"Project path '{project_path}' does not exist.")
        print(f"Error: Project path '{project_path}' does not exist.")
        return
    try:
        repo = git.Repo(project_path)
        status = repo.git.status()
        logging.info(f"Status checked for {project_path}")
        print(status)
    except git.exc.InvalidGitRepositoryError:
        logging.error(f"Error: '{project_path}' is not a valid Git repository.")
        print(f"Error: '{project_path}' is not a valid Git repository.")

def get_version(project_path):
    try:
        repo = git.Repo(project_path)
        tags = repo.git.tag()
        if tags:
            return sorted(tags.split(), key=lambda x: [int(y) for y in x.split('.')])[-1]  # Dernier tag
        return "v0.0.0"
    except git.exc.InvalidGitRepositoryError:
        logging.error(f"Cannot get version for {project_path}: Not a valid Git repository.")
        return "v0.0.0"

# Test Script
if __name__ == "__main__":
    config = load_config()
    if len(sys.argv) == 1:
        print("Usage: python3 app_manager.py <command> [args...]")
        print("Commands: create <project_name> <template> [--no-remote] [--no-git], create_branch <project_name> <branch_name>,")
        print("          merge_branch <project_name> <branch_name>, resolve_merge_conflict <project_name>,")
        print("          push_changes <project_name>, pull_changes <project_name>, list, delete <project_name>, list_commits <project_name>, status <project_name>")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    project_path = os.path.join(config["central_directory"], sys.argv[2]) if len(sys.argv) > 2 else None

    if command == "create" and len(sys.argv) >= 4:
        link_remote = "--no-remote" not in sys.argv
        init_git = "--no-git" not in sys.argv
        project_path = create_project(sys.argv[2], sys.argv[3], config, link_remote=link_remote, init_git=init_git)
        print(f"Project created at: {project_path}")
        print("Loaded config:", json.dumps(config, indent=2))
        save_config(config)
        print("Config file updated.")
    elif command == "create_branch" and len(sys.argv) == 4:
        create_branch(project_path, sys.argv[3])
    elif command == "merge_branch" and len(sys.argv) == 4:
        merge_branch(project_path, sys.argv[3])
    elif command == "resolve_merge_conflict" and len(sys.argv) == 3:
        resolve_merge_conflict_interactive(project_path)
    elif command == "push_changes" and len(sys.argv) == 3:
        push_changes(project_path, config)
    elif command == "pull_changes" and len(sys.argv) == 3:
        pull_changes(project_path, config)
    elif command == "list" and len(sys.argv) == 2:
        list_projects(config)
    elif command == "delete" and len(sys.argv) == 3:
        delete_project(sys.argv[2], config)
    elif command == "list_commits" and len(sys.argv) == 3:
        list_commits(project_path)
    elif command == "status" and len(sys.argv) == 3:
        status(project_path)
    else:
        print("Commande inconnue")