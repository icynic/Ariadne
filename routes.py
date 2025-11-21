# Run this file to open in browser (development mode)
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from lowlevel import (
    get_foreground_window,
    get_browser_address,
    bring_to_foreground,
    check_startup_entry,
    change_startup_entry,
    # close_app,
    
)
from files import (
    read_quests,
    write_quests,
    get_data_path,
    # read_controls,
    # write_controls,
    quest_template,
    # control_template,
    get_browser,
    set_browser,
    read_note,
    write_note
)
from daemon import start_daemon_thread, exe_to_time, address_to_time


app: Flask = Flask(__name__, static_url_path="", static_folder="frontend/dist")
CORS(app)  # Enable CORS for all routes


@app.get("/")
def getIndex() -> Response:
    return app.send_static_file("index.html")


@app.get("/api/quests")
def getQuests():
    return read_quests()


@app.post("/api/quests")
def postQuests():
    write_quests(request.get_json())
    return ""


@app.get("/api/quest-template")
def getQuestTemplate():
    return quest_template

# @app.get("/apu/control-template")
# def getControlTemplate():
#     return control_template


@app.get("/api/foreground-window")
def getForegroundWindow():
    return jsonify(get_foreground_window())


@app.get("/api/browser-address")
def getBrowserAddress():
    # return get_browser_address(get_browser())
    return get_browser_address()


@app.post("/api/bring-to-foreground")
def BringToForeground():
    bring_to_foreground(request.json["hwnd"])
    return ""

@app.get("/api/time-data")
def getTimeData():
    return [exe_to_time, address_to_time]


@app.get("/api/settings/startup")
def getStartup():
    return "true" if check_startup_entry() else "false"


@app.post("/api/settings/startup")
def changeStartup():
    change_startup_entry(request.json["isStartup"])
    return ""


@app.get("/api/settings/data-path")
def getDataPath():
    return get_data_path()

@app.get("/api/settings/browser")
def getBrowser():
    return get_browser()

@app.post("/api/settings/browser")
def postBrowser():
    set_browser(request.json["browser"])
    return ""

@app.get("/api/notes")
def getNote():
    return read_note()


@app.post("/api/notes")
def postNote():
    write_note(request.json)
    return ""

# @app.post("/api/close-app")
# def closeApp():
#     close_app(request.json["hwnd"])
#     return ""


# @app.get("/api/controls")
# def getControls():
#     return read_controls()


# @app.post("/api/controls")
# def postControls():
#     controls = request.get_json()
#     write_controls(controls)
#     return ""


if __name__ == "__main__":
    start_daemon_thread()
    app.run(host="127.0.0.1", port=5000, debug=True)
    # app.run(host="127.0.0.1", port=5000, debug=False)
