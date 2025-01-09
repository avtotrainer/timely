import sys
import configparser
import os
import base64
import requests
from schedule_generator import ClassSchedule
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
)


class ScheduleApp(QMainWindow):
    """
    Main application class for the schedule generator GUI.
    Reads configuration, generates schedule, and uploads it to GitHub.
    """

    def __init__(self):
        super().__init__()
        self.config = self.load_config()
        self.language = "ka"  # ენას ავირჩევთ აქ (ka ან en)
        self.translations = self.load_translations(self.language)

        self.init_ui()

    def load_config(self):
        """
        Loads the configuration from config.ini.
        Returns:
            dict: Dictionary containing configuration parameters.
        """
        config = configparser.ConfigParser()
        config.read("config.ini")
        return config["DEFAULT"]

    def load_translations(self, language="ka"):
        """
        ჩატვირთავს მხოლოდ მითითებულ ენის სექციას translations.ini ფაილიდან.

        Args:
            language (str): ენის კოდი (მაგ., "ka" ან "en").

        Returns:
            dict: მითითებული ენის სექცია.
        """
        lang_sections = configparser.ConfigParser()
        translations_path = os.path.join(os.path.dirname(__file__), "translations.ini")
        lang_sections.read(translations_path)

        # თუ სექცია არსებობს, დავაბრუნოთ ის, სხვა შემთხვევაში გამონაკლისი
        if language in lang_sections:
            return dict(
                lang_sections[language]
            )  # ვაბრუნებთ კონკრეტული ენის სექციის მონაცემებს
        else:
            raise KeyError(f"სექცია '{language}' არ მოიძებნა translations.ini ფაილში.")

    def translate(self, key):
        """
        თარგმნისთვის გამოსაყენებელი ფუნქცია.

        Args:
            key (str): გასაღები.

        Returns:
            str: თარგმანი ან სარეზერვო ტექსტი.
        """
        return self.translations.get(key, key)  # თუ გასაღები არ მოიძებნა, დაბრუნდეს key

    def init_ui(self):
        """
        გრაფიკული ინტერფეისის ინიციალიზაცია.
        """
        self.setWindowTitle(self.translate("generate_and_upload"))
        layout = QVBoxLayout()
        self.inputs = {}

        # დავამატოთ ტექსტები ქართულად
        for key, value in self.config.items():
            if key in ["github_token", "github_repo"]:  # არ ვაჩვენებთ ამ ველებს
                continue
            label = QLabel(self.translate(key))
            input_field = QLineEdit(value)
            layout.addWidget(label)
            layout.addWidget(input_field)
            self.inputs[key] = input_field

        # დავამატოთ ღილაკი "შექმნა და ატვირთვა"
        self.generate_button = QPushButton(self.translate("generate_and_upload"))
        self.generate_button.clicked.connect(self.generate_and_upload)
        layout.addWidget(self.generate_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def generate_and_upload(self):
        """
        Generates the schedule file based on user input and
        uploads it to GitHub.
        """
        # Gather parameters from GUI inputs
        params = {key: input_field.text() for key, input_field in self.inputs.items()}
        schedule = ClassSchedule(
            start_time=params["start_time"],
            lesson_duration=int(params["lesson_duration"]),
            short_break=int(params["short_break"]),
            long_break_after=int(params["long_break_after"]),
            long_break=int(params["long_break"]),
            total_lessons=int(params["total_lessons"]),
        )

        # Generate schedule file
        file_name = schedule.generate_schedule(params["school_code"])

        # Upload file to GitHub
        github_repo = self.config["github_repo"]
        # github_token = self.config["github_token"]

        github_token = os.getenv("GITHUB_TOKEN")

        if not github_token:
            print("შეცდომა: GITHUB_TOKEN გარემოს ცვლადი არ არის განსაზღვრული.")
            return
        self.upload_to_github(file_name, github_repo, github_token)

    def upload_to_github(self, file_path, repo, token):
        """
        Uploads the generated file to the specified GitHub repository.
        Handles existing files by retrieving their SHA and overwriting.

        Args:
            file_path (str): Path to the file to upload.
            repo (str): GitHub repository in the format "user/repo".
            token (str): GitHub API token.
        """
        # Read file content and encode it in Base64
        with open(file_path, "rb") as file:
            content = base64.b64encode(file.read()).decode("utf-8")

        url = f"https://api.github.com/repos/{repo}/contents/{os.path.basename(file_path)}"
        headers = {"Authorization": f"token {token}"}

        # Check if the file already exists to retrieve its SHA
        response = requests.get(url, headers=headers)
        if response.status_code == 200:  # File exists
            file_sha = response.json()["sha"]
        elif response.status_code == 404:  # File does not exist
            file_sha = None
        else:
            print(f"Failed to check file existence: {response.text}")
            return

        # Prepare data for upload
        data = {
            "message": "Updated schedule",
            "content": content,
            "branch": "main",
        }
        if file_sha:
            data["sha"] = file_sha  # Add SHA if file exists

        # Upload the file
        response = requests.put(url, headers=headers, json=data)
        if response.status_code in [200, 201]:
            print("File uploaded successfully.")
        else:
            print(f"Failed to upload file: {response.text}")


if __name__ == "__main__":
    """
    Entry point of the application. Supports both GUI and CLI modes.
    """
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        # CLI Mode
        config = configparser.ConfigParser()
        config.read("config.ini")
        params = config["DEFAULT"]
        schedule = ClassSchedule(
            start_time=params["start_time"],
            lesson_duration=int(params["lesson_duration"]),
            short_break=int(params["short_break"]),
            long_break_after=int(params["long_break_after"]),
            long_break=int(params["long_break"]),
            total_lessons=int(params["total_lessons"]),
        )
        file_name = schedule.generate_schedule(params["school_code"])
        ScheduleApp.upload_to_github(
            None, file_name, params["github_repo"], params["github_token"]
        )
    else:
        # GUI Mode
        app = QApplication(sys.argv)
        window = ScheduleApp()
        window.show()
        sys.exit(app.exec())
