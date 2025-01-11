import base64
import requests
import os


class Uploader:
    def __init__(self, repo, token):
        self.repo = repo
        self.token = token

    def upload_file(self, file_path, content):
        """
        Uploads a file to GitHub. Retrieves `sha` if the file exists.

        Args:
            file_path (str): Name of the file to upload.
            content (str): Content of the file.

        Raises:
            Exception: If the upload fails.
        """
        url = f"https://api.github.com/repos/{self.repo}/contents/{os.path.basename(file_path)}"
        headers = {"Authorization": f"token {self.token}"}

        # Check if the file already exists to retrieve its SHA
        response = requests.get(url, headers=headers)
        if response.status_code == 200:  # File exists
            file_sha = response.json().get("sha")
        elif response.status_code == 404:  # File does not exist
            file_sha = None
        else:
            raise Exception(
                f"Failed to check file existence: {response.status_code}, {response.text}"
            )

        # Prepare data for upload
        data = {
            "message": "Updated schedule",
            "content": base64.b64encode(content.encode("utf-8")).decode("utf-8"),
            "branch": "main",
        }
        if file_sha:
            data["sha"] = file_sha  # Add SHA if file exists

        # Upload the file
        response = requests.put(url, headers=headers, json=data)
        if response.status_code in [200, 201]:
            print("File uploaded successfully.")
        else:
            raise Exception(
                f"Failed to upload file: {response.status_code}, {response.text}"
            )
