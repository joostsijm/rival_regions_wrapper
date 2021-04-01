import os
import errno
from selenium_stealth import stealth
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webbot import Browser

class StealthBrowser(Browser):
    """

    **Constructor**


    :__init__(showWindow = True , proxy = None):
        The constructor takes showWindow flag as argument which Defaults to False. If it is set to true , all browser happen without showing up any GUI window .

        :Args:
            - showWindow : If true , will run a headless browser without showing GUI window.
            - proxy : Url of any optional proxy server.



    Object attributes:  Key , errors

    :Key:
        - It contains the constants for all the special keys in the keyboard which can be used in the *press* method
    errors:
        - List containing all the errors which might have occurred during performing an action like click ,type etc.
    """

    def __init__(self, showWindow=True, proxy=None , downloadPath:str=None):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument("user-agent=DN")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        if downloadPath is not None and isinstance(downloadPath,str):
            absolutePath = os.path.abspath(downloadPath)
            if(not os.path.isdir(absolutePath)):
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), absolutePath)

            options.add_experimental_option('prefs', {'download.default_directory' : absolutePath})

        if proxy is not None and isinstance(proxy, str):
            options.add_argument("--proxy-server={}".format(proxy))

        if not showWindow:
            options.headless = True

        self.driver = webdriver.Chrome(options=options)
        self.Key = Keys
        self.errors = []
        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        [setattr(self, function, getattr(self.driver, function)) for function in
         ['add_cookie', 'delete_all_cookies', 'delete_cookie', 'execute_script', 'execute_async_script',
          'fullscreen_window', 'get_cookie', 'get_cookies', 'get_log', 'get_network_conditions',
          'get_screenshot_as_base64', 'get_screenshot_as_file', 'get_screenshot_as_png', 'get_window_position',
          'get_window_rect', 'get_window_size', 'maximize_window', 'minimize_window', 'implicitly_wait', 'quit',
          'refresh', 'save_screenshot', 'set_network_conditions', 'set_page_load_timeout', 'set_script_timeout',
          'set_window_position', 'set_window_rect', 'start_client', 'start_session', 'stop_client', 'switch_to_alert']]






