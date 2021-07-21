"""Login methods"""

import time

import requests
from python_anticaptcha import ImageToTextTask
from selenium.common.exceptions import NoSuchElementException

from rival_regions_wrapper import LOGGER, DATA_DIR
from rival_regions_wrapper.browser import Browser
from rival_regions_wrapper.exceptions import (
    NoCaptchaClientException,
    LoginException,
)


# This should be working
def login_google(show_window, username, password, captcha_client=None):
    """login using Google"""
    browser = Browser(show_window, DATA_DIR, "g_{}".format(username))
    LOGGER.info('Google: "%s": Login start', username)
    try:
        # browser = Browser(show_window, DATA_DIR, 'g_{}'.format(username))
        browser.go_to("https://rivalregions.com/")
        google_login_link = browser.driver.find_element_by_css_selector(
            ".sa_link.gogo"
        ).get_attribute("href")
        browser.go_to(google_login_link)
        time.sleep(0.5)
    except NoSuchElementException:
        LOGGER.info('Google: "%s": still RR session active', username)
        return browser

    # browser.get_screenshot_as_file('test_1.png')

    if browser.driver.find_elements_by_css_selector("#gold"):
        LOGGER.info('Google: "%s": account already logged in', username)
        return browser

    LOGGER.info('Google: "%s": Typing in username', username)
    if not browser.driver.find_elements_by_css_selector("#Email"):
        LOGGER.info('Google: "%s": problem with fill in password', username)
        raise LoginException() from NoSuchElementException
    browser.type(username, css_selector="#Email")

    # browser.get_screenshot_as_file('test_2.png')

    LOGGER.info('Google: "%s": pressing next button', username)
    browser.click(css_selector="#next")
    time.sleep(0.5)

    # browser.get_screenshot_as_file('test_3.png')

    while browser.driver.find_elements_by_css_selector("#captcha-box"):
        LOGGER.info('Google: "%s": Captcha present', username)
        if not captcha_client:
            raise NoCaptchaClientException()
        captcha_url = browser.find_elements(css_selector="#captcha-img img")[
            0
        ].get_attribute("src")
        LOGGER.debug('Google: "%s": Captcha url: "%s"', username, captcha_url)
        image = requests.get(captcha_url, stream=True).raw
        image.decode_content = True

        job = captcha_client.createTask(ImageToTextTask(image))
        LOGGER.info('Google: "%s": Start solve captcha', username)
        job.join()
        LOGGER.info(
            'Google: "%s": captcha: "%s"', username, job.get_captcha_text()
        )
        browser.type(
            job.get_captcha_text(), css_selector="#identifier-captcha-input"
        )
        browser.click(css_selector="#next")
        time.sleep(0.5)

        # browser.get_screenshot_as_file('test_4.png')

    if not browser.driver.find_elements_by_css_selector("#password"):
        LOGGER.info('Google: "%s": browser security issue', username)
        if show_window:
            browser.new_tab("https://accounts.google.com/")
            LOGGER.info('Google: "%s": fill in credentials', username)
            while not browser.driver.find_elements_by_css_selector("#gold"):
                time.sleep(2)
                LOGGER.info(
                    'Google: "%s": waiting to fill in credentials', username
                )
                browser.go_to(google_login_link)
            return browser
        raise LoginException()

    # with open('source.html', 'w') as source:
    #     source.write(browser.get_page_source())

    LOGGER.info('Google: "%s": Typing in password', username)
    browser.type(password, css_selector="input")

    # browser.get_screenshot_as_file('test_5.png')

    LOGGER.info('Google: "%s": pressing sign in button', username)
    browser.click(css_selector="#submit")
    time.sleep(0.5)

    # browser.get_screenshot_as_file('test_6.png')

    return browser


# IDK if this is working
def login_vk(show_window, username, password, captcha_client=None):
    """login using VK"""
    browser = Browser(show_window, DATA_DIR, "vk_{}".format(username))
    LOGGER.info("Login method VK")
    browser.go_to("https://rivalregions.com/")
    browser.click(css_selector=".sa_sn.imp.float_left")
    time.sleep(1)

    browser.type(username, into="email")
    browser.type(
        password, xpath="/html/body/div/div/div/div[2]/form/div/div/input[7]"
    )
    browser.click("Log in")
    return browser


# IDK if this is working
def login_facebook(show_window, username, password, captcha_client=None):
    """login using Facebook"""
    browser = Browser(show_window, DATA_DIR, "fb_{}".format(username))
    LOGGER.info("Login method Facebook")
    browser.go_to("https://rivalregions.com/")
    browser.click(css_selector="sa_sn.float_left.imp.vkvk")
    time.sleep(1)

    browser.type(username, into="Email")
    browser.type(password, into="Password")
    browser.click("Log In")
    time.sleep(5)
    browser.click(css_selector=".sa_sn.imp.float_left")
    return browser
