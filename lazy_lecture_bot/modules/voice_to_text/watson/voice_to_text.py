import json
import os

import requests
from modules import file_utilities

CREDENTIALS_PATH = file_utilities.abs_resource_path(["credentials", "ibm_watson.json"])


def get_credentials():
    if "watson_url" not in os.environ or "watson_password" not in os.environ or "watson_username" not in os.environ:
        with open(CREDENTIALS_PATH, 'r') as fh:
            credentials = json.load(fh)["credentials"]
    else:
        credentials = {
            "url": os.environ["watson_url"],
            "username": os.environ["watson_username"],
            "password": os.environ["watson_password"],
        }

    return credentials


def transcribe(audio, credentials):
    endpoint = credentials["url"] + "/v1/recognize"
    auth = (credentials["username"], credentials["password"])
    headers = {"Content-Type": "audio/wav"}
    params = {"continuous": "true", "timestamps": "true", "inactivity_timeout": "-1", "profanity_filter": "false"}
    r = requests.post(endpoint, data=audio, headers=headers, auth=auth, params=params)
    r.raise_for_status()

    return r.json()


if __name__ == "__main__":
    creds = get_credentials()
    print(transcribe(file_utilities.abs_resource_path(
        ["test_videos", "16Khz_50_sec_audio_cpp_example.mp4.wav"]), creds))
