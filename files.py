import json
import os
from icecream import ic

# Ensure the directory exists
dir_path = os.path.join(os.getenv("APPDATA"), "Ariadne")
os.makedirs(dir_path, exist_ok=True)
file_path = os.path.join(dir_path, "data.json")


quest_template: dict = {"title": "", "text": "", "completeTimes": 0}
# control_template: dict = {"title": "close", "target": "target", "time": 5}

data_template: dict = {
    "quests": {
        "entities": [],
        "active": [],
        "available": [],
        "completed": [],
    },
    # "controls": [control_template],
    "settings": {"browser": ""},
    "note": [{"name": "note", "text":""}]
}


# Create the file if it doesn't exist, or if the file is empty
def _create_data_if_not_exists():
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        try:
            with open(file_path, "w") as f:
                json.dump(data_template, f)
        except Exception as e:
            print(f"Unexpected error when creating data file: {e}")


def _read_data() -> dict:
    _create_data_if_not_exists()
    with open(file_path, "r") as f:
        return json.load(f)


def read_quests() -> dict:
    return _read_data()["quests"]


def _write_data(data: dict):
    with open(file_path, "w") as f:
        json.dump(data, f)


def write_quests(quests: dict):
    data: dict = _read_data()
    data["quests"] = quests
    _write_data(data)


def get_data_path() -> str:
    return file_path


# def read_controls() -> list:
#     _create_data_if_not_exists()
#     return _read_data()["controls"]


# def write_controls(controls: list):
#     data: dict = _read_data()
#     data["controls"] = controls
#     _write_data(data)

browser_stored: str = ""


def get_browser() -> str:
    global browser_stored
    if not browser_stored:
        data: dict = _read_data()
        browser_stored = data["settings"]["browser"]
    return browser_stored


def set_browser(browser: str):
    data: dict = _read_data()
    data["settings"]["browser"] = browser
    _write_data(data)
    global browser_stored
    browser_stored = browser


def read_note() -> dict:
    return _read_data()["note"]


def write_note(note: dict):
    data: dict = _read_data()
    data["note"] = note
    _write_data(data)
    



if __name__ == "__main__":
    # print(read_quests())
    # write_quests([{"id": 1, "title": "hello", "text": "world"}])
    # print(read_quests())
    from daemon import start_daemon_thread, exe_to_time
    import time

    start_daemon_thread()
    while True:
        time.sleep(100)
