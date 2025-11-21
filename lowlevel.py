import win32gui
import win32process
import win32api
import win32con
import time
import pywinauto
import sys
import winreg
from icecream import ic
from files import get_browser


def get_foreground_window() -> dict[str, int | str]:
    hwnd: int = win32gui.GetForegroundWindow()
    text: str = win32gui.GetWindowText(hwnd)
    executable = _get_window_executable(hwnd)
    return {"hwnd": hwnd, "text": text, "executable": executable}


def _get_window_executable(hwnd: int) -> str:
    _, process_id = win32process.GetWindowThreadProcessId(hwnd)
    try:
        process_handle: int = win32api.OpenProcess(
            # win32con.PROCESS_ALL_ACCESS,
            # win32con.PROCESS_QUERY_INFORMATION,
            win32con.PROCESS_QUERY_LIMITED_INFORMATION,
            False,
            process_id,
        )
        executable_path: str = win32process.GetModuleFileNameEx(process_handle, 0)
        win32api.CloseHandle(process_handle)
        return executable_path
    except Exception as e:
        print("Exception of getting executable name: ", e)
        return ""


def bring_to_foreground(hwnd: int) -> None:
    try:
        win32gui.SetForegroundWindow(hwnd)
    except Exception as e:
        print("Exception of bringing window to foreground: ", e)


address_bar = None
browser = None
app = None
browser_to_regular: dict = {
    "Chrome": ".*Google Chrome$",
    "Firefox": ".*Mozilla Firefox$",
    "Edge": ".*Microsoft\u200b Edge$",
}


def get_browser_regular() -> str:
    return browser_to_regular.get(get_browser(), "")


def get_browser_address() -> str:
    if not get_browser_regular():
        ic("can't find browser")
        return ""
    try:
        backend: str = "uia"
        global address_bar
        global browser
        global app
        if app and not app.is_process_running():
            app = None
            address_bar = None
            return "Browser Closed"
        if not address_bar or browser != get_browser() or not app:
            app = pywinauto.Application(backend=backend).connect(
                title_re=get_browser_regular()
            )
            main_window = app.top_window()
            all_edits = main_window.descendants(control_type="Edit")
            # Assuming the address bar is the first edit control, get its value
            address_bar = all_edits[0]
            browser = get_browser()
        if address_bar.get_value() == "":
            return "New Tab"
        else:
            return address_bar.get_value()
    except pywinauto.findwindows.ElementNotFoundError:
        ic("element not found")
        return ""
    except Exception as e:
        ic(e)
        return ""


executable_path = sys.executable
reg_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
entry_name = "Ariadne"


def change_startup_entry(isAdd: bool) -> None:
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_key, 0, winreg.KEY_SET_VALUE)
        if isAdd:
            winreg.SetValueEx(key, entry_name, 0, winreg.REG_SZ, executable_path)
        else:
            winreg.DeleteValue(key, entry_name)
        winreg.CloseKey(key)
    except Exception as e:
        pass


def check_startup_entry() -> bool:
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_key, 0, winreg.KEY_READ)
        value, reg_type = winreg.QueryValueEx(key, entry_name)
        if value == executable_path:
            winreg.CloseKey(key)
            return True
        winreg.CloseKey(key)
        return False
    except Exception as e:
        return False


def close_app(hwnd: int) -> None:
    _, process_id = win32process.GetWindowThreadProcessId(hwnd)
    try:
        process_handle: int = win32api.OpenProcess(
            win32con.PROCESS_TERMINATE,
            False,
            process_id,
        )
        win32api.TerminateProcess(process_handle, -1)
        win32api.CloseHandle(process_handle)
    except Exception as e:
        print("Exception of clossing app: ", e)



if __name__ == "__main__":
    # sum=0
    times = 3
    for i in range(times):
        a = time.time()
        print(get_browser_address("Firefox"))
        b = time.time()
        # sum+=b-a
        time.sleep(2)
    # ic(sum/times)
