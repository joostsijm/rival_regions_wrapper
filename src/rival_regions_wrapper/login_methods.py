"""Login methods"""

import time

import requests
from python_anticaptcha import ImageToTextTask

from rival_regions_wrapper import LOGGER
from rival_regions_wrapper.exceptions import NoCaptchaClientException, \
        LoginException


# This should be working
def login_google(browser, auth_text, username, password, captcha_client=None):
    """login using Google"""
    LOGGER.info('Google: "%s": Login start', username)
    auth_text1 = auth_text.split('\t<a href="')
    auth_text2 = auth_text1[1].split('" class="sa')
    time.sleep(1)
    browser.go_to(auth_text2[0])

    # browser.get_screenshot_as_file('test_1.png')

    LOGGER.info('Google: "%s": Typing in username', username)
    browser.type(username, into='Email')

    # browser.get_screenshot_as_file('test_2.png')

    LOGGER.info('Google: "%s": pressing next button', username)
    browser.click(css_selector='#next')
    time.sleep(1)

    # browser.get_screenshot_as_file('test_3.png')

    if browser.driver.find_elements_by_css_selector('#captcha-box'):
        LOGGER.info('Google: "%s": Captcha present', username)
        if not captcha_client:
            raise NoCaptchaClientException()
        captcha_url = browser \
                .find_elements(css_selector='#captcha-img img')[0] \
                .get_attribute('src')
        LOGGER.debug('Google: "%s": Captcha url: "%s"', username, captcha_url)
        image = requests.get(captcha_url, stream=True).raw
        image.decode_content = True

        task = ImageToTextTask(image)
        job = captcha_client.createTask(task)
        LOGGER.info('Google: "%s": Start solve captcha', username)
        job.join()

        LOGGER.info('Google: %s": captcha: "%s"', username, job.get_captcha_text())
        browser.type(
                job.get_captcha_text(),
                css_selector='#identifier-captcha-input'
            )
        browser.click(css_selector='#next')

        # browser.get_screenshot_as_file('test_4.png')

    if not browser.driver.find_elements_by_css_selector('#password'):
        raise LoginException()

    # with open('source.html', 'w') as source:
    #     source.write(browser.get_page_source())

    LOGGER.info('Google: "%s": Typing in password', username)
    browser.type(password, css_selector='input')

    # browser.get_screenshot_as_file('test_5.png')

    LOGGER.info('Google: "%s": pressing sign in button', username)
    browser.click(css_selector='#submit')
    time.sleep(3)

    # browser.get_screenshot_as_file('test_6.png')

    # Some why it wont click and login immediately. This seems to work
    browser.go_to(auth_text2[0])
    time.sleep(1)

    # browser.get_screenshot_as_file('test_7.png')

    browser.go_to(auth_text2[0])
    time.sleep(1)

    # browser.get_screenshot_as_file('test_8.png')

    browser.click(
        css_selector='#sa_add2 > div:nth-child(4) > a.sa_link.gogo > div'
    )
    time.sleep(2)

    # browser.get_screenshot_as_file('test_9.png')

    return browser


# IDK if this is working
def login_vk(browser, auth_text, username, password, captcha_client=None):
    """login using VK"""
    LOGGER.info('Login method VK')
    auth_text1 = auth_text.split("(\'.vkvk\').attr(\'url\', \'")
    auth_text2 = auth_text1[1].split('&response')

    browser.go_to(auth_text2[0])
    browser.type(username, into='email')
    browser.type(
            password,
            xpath="/html/body/div/div/div/div[2]/form/div/div/input[7]"
    )
    browser.click('Log in')
    return browser


# IDK if this is working
def login_facebook(browser, auth_text, username, password, captcha_client=None):
    """login using Facebook"""
    LOGGER.info('Login method Facebook')
    auth_text1 = \
        auth_text.split('">\r\n\t\t\t\t<div class="sa_sn imp float_left" ')
    auth_text2 = auth_text1[0].split('200px;"><a class="sa_link" href="')
    url = auth_text2[1]

    browser.go_to(url)
    browser.type(username, into='Email')
    browser.type(password, into='Password')
    browser.click('Log In')
    time.sleep(5)
    browser.click(css_selector='.sa_sn.imp.float_left')
    return browser
