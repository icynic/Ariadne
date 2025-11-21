import threading
from icecream import ic
import time
from lowlevel import get_foreground_window, get_browser_regular, get_browser_address
# from files import get_browser
import re


daemon_thread: threading.Thread | None = None
exe_to_time: dict[str, list[tuple[float, float]]] = {}
address_to_time: dict[str, list[tuple[float, float]]] = {}
stop_flag: threading.Event = threading.Event()
is_browser_terminated: bool = False


def parseURL(url:str):
    remainder=url
    if "//" in url:
        remainder = url.split('//', 1)[1]
        if remainder.startswith('/'):
            return remainder.split('/')[-1]
    remainder = remainder.split('/', 1)[0]
    return remainder

def add_record(old:list, new:str, table:dict):
    current_time: float = time.time()
    if new not in table:
        table[new] = [[current_time, current_time]]
    elif new != old[0]:
        table[new].append([current_time, current_time])
    if old[0] in table:
        table[old[0]][-1][1] = current_time
    old[0] = new

def start_daemon_thread(sleep_time=5) -> None:
    global daemon_thread, stop_flag

    # Signal the existing thread to stop if it's running
    if daemon_thread and daemon_thread.is_alive():
        ic("Stopping existing daemon thread")
        stop_flag.set()
        daemon_thread.join(timeout=sleep_time)
        if daemon_thread.is_alive():
            ic("Failed to stop the existing daemon thread")
    # Reset the stop flag for the new thread
    stop_flag.clear()

    def check_system_state():
        global is_browser_terminated
        
        previous_executable:list = [""]
        previous_address:list=[""]
        while not stop_flag.is_set():
            window: dict[str, int | str] = get_foreground_window()
            title:str=window["text"]
            # hwnd: int = window["hwnd"]
            executable: str = window["executable"]
            
            add_record(previous_executable, executable, exe_to_time)
            
            if get_browser_regular() and re.search(get_browser_regular(), title):
                address=parseURL(get_browser_address())
                add_record(previous_address, address, address_to_time)
                # ic(address)    
                is_browser_terminated=False
            elif not is_browser_terminated:
                address=parseURL(get_browser_address())
                add_record(previous_address, address, address_to_time)
                is_browser_terminated=True
                
                
            stop_flag.wait(timeout=sleep_time)

    daemon_thread = threading.Thread(target=check_system_state)
    daemon_thread.daemon = True
    daemon_thread.start()

if __name__ == "__main__":
    start_daemon_thread()
    while True:
        time.sleep(100)
    
