import json
import os
import threading

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CANDIDATES_FILE = os.path.join(BASE_DIR, "candidates.json")
SUMMARY_FILE = os.path.join(BASE_DIR, "summary.json")

file_lock = threading.Lock()


def read_json(file_path, default):
    if not os.path.exists(file_path):
        return default

    with file_lock:
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return default


def write_json(file_path, data):
    with file_lock:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)