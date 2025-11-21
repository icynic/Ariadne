# Run this file to open in webview window (deployment mode)
import webview
from routes import app
from daemon import start_daemon_thread
from os import _exit
import pystray
from PIL import Image
from lowlevel import get_browser_regular, get_browser_address

def custom_logic(window):
    # Hide the scroll bar
    window.evaluate_js(
        """
                        const style = document.createElement('style');
                        style.innerHTML = `::-webkit-scrollbar { display: none; }`;
                        document.head.appendChild(style);
                        """
    )
    window.expose(hide, close)
    window.expose(get_browser_address, get_browser_regular)
    icon.run()


def show():
    window.show()
    window.restore()


def close():
    window.destroy()
    icon.stop()
    _exit(0)


def hide():
    window.minimize()
    window.hide()


# Icon
image = Image.open(r"C:\Users\effax\Pictures\图层 1.png").resize((100, 100))
menu = (
    pystray.MenuItem("Show Interface", show, default=True),
    pystray.MenuItem("Exit", close),
)
icon = pystray.Icon("Ariadne", image, "Ariadne", menu, on_click=show)
icon.on_click = show


start_daemon_thread()
window = webview.create_window(
    title="Ariadne",
    url=app,
    # url="frontend/dist/index.html",
    frameless=True,
    easy_drag=False,
    resizable=True,
    # transparent=True
)
# webview.start(custom_logic, window, debug=True)
webview.start(custom_logic, window)
