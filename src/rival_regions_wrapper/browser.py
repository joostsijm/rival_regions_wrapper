"""
Browser module
"""

from selenium_stealth import stealth
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import webbot


class Browser(webbot.Browser):
    """Browser class"""

    def __init__(
        self, show_window=True, data_dir="chrome", username="Profile 1"
    ):

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("user-agent=DN")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"]
        )
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--user-data-dir={}/chrome".format(data_dir))
        options.add_argument("--profile-directory={}".format(username))

        if not show_window:
            options.headless = True

        self.driver = webdriver.Chrome(options=options)
        self.Key = Keys
        self.errors = []
        stealth(
            self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

        for function in [
            "add_cookie",
            "delete_all_cookies",
            "delete_cookie",
            "execute_script",
            "execute_async_script",
            "fullscreen_window",
            "get_cookie",
            "get_cookies",
            "get_log",
            "get_network_conditions",
            "get_screenshot_as_base64",
            "get_screenshot_as_file",
            "get_screenshot_as_png",
            "get_window_position",
            "get_window_rect",
            "get_window_size",
            "maximize_window",
            "minimize_window",
            "implicitly_wait",
            "quit",
            "refresh",
            "save_screenshot",
            "set_network_conditions",
            "set_page_load_timeout",
            "set_script_timeout",
            "set_window_position",
            "set_window_rect",
            "start_client",
            "start_session",
            "stop_client",
            "switch_to_alert",
        ]:
            setattr(self, function, getattr(self.driver, function))

    def add_cookie(self, cookie):
        """To pretent lint error"""
        self.add_cookie(cookie)

    def refresh(self):
        """To pretent lint error"""
        self.refresh()
