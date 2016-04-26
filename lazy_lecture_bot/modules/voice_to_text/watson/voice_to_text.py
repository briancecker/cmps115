import json

import requests
from modules import file_utilities

CREDENTIALS_PATH = file_utilities.abs_resource_path(["credentials", "ibm_watson.json"])


def get_credentials():
    with open(CREDENTIALS_PATH, 'r') as fh:
        credentials = json.load(fh)["credentials"]

    return credentials


def transcribe_file(path, credentials):
    endpoint = credentials["url"] + "/v1/recognize"
    auth = (credentials["username"], credentials["password"])
    headers = {"Content-Type": "audio/wav"}
    params = {"continuous": "true", "timestamps": "true", "inactivity_timeout": "-1", "profanity_filter": "false"}
    with open(path, 'rb') as payload:
        r = requests.post(endpoint, data=payload, headers=headers, auth=auth, params=params)
    r.raise_for_status()

    return r.json()


if __name__ == "__main__":
    creds = get_credentials()
    print(transcribe_file(file_utilities.abs_resource_path(
        ["test_videos", "16Khz_50_sec_audio_cpp_example.mp4.wav"]), creds))
