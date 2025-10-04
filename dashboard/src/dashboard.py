import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QProgressBar, QMessageBox
from PyQt6.QtGui import QPalette, QColor
from app_manager import load_config, push_changes, pull_changes, status, list_commits, get_version, authenticate
import git

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = self.login()
        if not self.config:
            sys.exit(1)
        # Push all projects at startup
        self.push_all_projects()
        self.setWindowTitle("Dashboard Grok")
        self.setGeometry(100, 100, 800, 600)

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
        self.setPalette(palette)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.grid = QGridLayout()
        layout.addLayout(self.grid)

        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.update_dashboard)
        layout.addWidget(refresh_button)

        self.update_dashboard()

    def login(self):
        while True:
            username = input("Username: ")
            password = input("Password: ")
            if authenticate(username, password):
                print("Login successful!")
                return load_config()
            print("Invalid credentials. Try again.")

    def push_all_projects(self):
        projects = [d for d in os.listdir(self.config["central_directory"]) if os.path.isdir(os.path.join(self.config["central_directory"], d))]
        for project in projects:
            project_path = os.path.join(self.config["central_directory"], project)
            try:
                print(f"Pushing changes for {project}...")
                push_changes(project_path, self.config)
                print(f"Push completed for {project}.")
            except Exception as e:
                print(f"Failed to push {project}: {e}")

    def update_dashboard(self):
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setParent(None)

        projects = [d for d in os.listdir(self.config["central_directory"]) if os.path.isdir(os.path.join(self.config["central_directory"], d))]
        row = 0
        col = 0
        for project in projects:
            project_path = os.path.join(self.config["central_directory"], project)
            card = QWidget()
            card_layout = QVBoxLayout(card)
            card.setStyleSheet("border: 2px solid #333; padding: 10px; margin: 5px; background-color: white;")

            title = QLabel(project)
            title.setStyleSheet("font-weight: bold;")
            card_layout.addWidget(title)

            try:
                repo = git.Repo(project_path)
                commits = list_commits(project_path)
                progress = QProgressBar()
                progress.setValue(min(100, len(commits) * 10))  # Simplifié, à améliorer
                card_layout.addWidget(progress)
                version = QLabel(f"Version: {get_version(project_path)}")
                card_layout.addWidget(version)
            except Exception as e:
                progress = QProgressBar()
                progress.setValue(0)
                card_layout.addWidget(progress)
                version = QLabel("Version: v0.0.0 (Error)")
                card_layout.addWidget(version)

            features = QLabel("Features: TBD")
            card_layout.addWidget(features)

            open_button = QPushButton("Open")
            open_button.clicked.connect(lambda checked, p=project_path: self.open_project(p))
            card_layout.addWidget(open_button)

            push_button = QPushButton("Push")
            push_button.clicked.connect(lambda checked, p=project_path: self.push_project(p))
            card_layout.addWidget(push_button)

            pull_button = QPushButton("Pull")
            pull_button.clicked.connect(lambda checked, p=project_path: self.pull_project(p))
            card_layout.addWidget(pull_button)

            status_button = QPushButton("Status")
            status_button.clicked.connect(lambda checked, p=project_path: self.show_status(p))
            card_layout.addWidget(status_button)

            self.grid.addWidget(card, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

    def open_project(self, project_path):
        if os.path.exists(project_path):
            os.system(f"xdg-open {project_path}")
        else:
            QMessageBox.critical(self, "Error", f"Path {project_path} does not exist")

    def push_project(self, project_path):
        try:
            push_changes(project_path, self.config)
            QMessageBox.information(self, "Success", "Push completed successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Push failed: {e}")

    def pull_project(self, project_path):
        try:
            pull_changes(project_path, self.config)
            QMessageBox.information(self, "Success", "Pull completed successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Pull failed: {e}")

    def show_status(self, project_path):
        try:
            status(project_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Status check failed: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec())