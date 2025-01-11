import configparser
import os
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
)
from classes import ClassSchedule, Uploader

# from classes.uploader import Uploader


class ScheduleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = self.load_config()
        self.language = "ka"  # Default language: Georgian
        self.translations = self.load_translations(self.language)
        self.init_ui()

    

    def load_config(self):
        """
        Loads the configuration from config.ini.
        """
        config = configparser.ConfigParser()
        config.read("config.ini")  # Ensure the correct path to config.ini
        return config["DEFAULT"]

    def load_translations(self, language="ka"):
        """
        Loads translations from translations.ini for the specified language.
        """
        lang_sections = configparser.ConfigParser()
        translations_path = os.path.join(os.path.dirname(__file__), "translations.ini")
        lang_sections.read(translations_path)

        if language in lang_sections:
            return dict(lang_sections[language])
        else:
            raise KeyError(
                f"Translation section '{language}' not found in translations.ini"
            )

    def translate(self, key):
        """
        Translates a given key using the loaded translations.
        """
        return self.translations.get(
            key, key
        )  # Default to key if translation not found

    def init_ui(self):
        """
        Initializes the GUI and populates fields with default values and translations.
        """
        self.setWindowTitle(self.translate("generate_and_upload"))
        layout = QVBoxLayout()
        self.inputs = {}

        # Add input fields with default values and translations
        for key, value in self.config.items():
            if key in ["github_token", "github_repo"]:  # Skip sensitive fields
                continue
            label = QLabel(self.translate(key))
            input_field = QLineEdit(value)  # Set default value
            layout.addWidget(label)
            layout.addWidget(input_field)
            self.inputs[key] = input_field

        # Add "Generate and Upload" button
        self.generate_button = QPushButton(self.translate("generate_and_upload"))
        self.generate_button.clicked.connect(self.generate_and_upload)
        layout.addWidget(self.generate_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def generate_and_upload(self):
        """
        Generates a schedule and uploads it to GitHub.
        """
        # Gather inputs
        params = {key: field.text() for key, field in self.inputs.items()}
        schedule = ClassSchedule(
            start_time=params["start_time"],
            lesson_duration=int(params["lesson_duration"]),
            short_break=int(params["short_break"]),
            long_break_after=int(params["long_break_after"]),
            long_break=int(params["long_break"]),
            total_lessons=int(params["total_lessons"]),
        )

        # Generate schedule
        schedule_data, file_name = schedule.generate_schedule(params["school_code"])
        with open(file_name, "w") as file:
            file.write("\n".join(schedule_data))

        # Upload to GitHub
        github_repo = self.config["github_repo"]
        github_token = self.config.get("github_token", os.getenv("GITHUB_TOKEN"))
        if not github_token:
            print(self.translate("error_no_github_token"))
            return
        uploader = Uploader(repo=github_repo, token=github_token)
        uploader.upload_file(file_name, "\n".join(schedule_data))


if __name__ == "__main__":
    app = QApplication([])
    window = ScheduleApp()
    window.show()
    app.exec()
