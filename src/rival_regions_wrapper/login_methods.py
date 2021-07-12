"""Login methods"""

import time

from rival_regions_wrapper import LOGGER


# This should be working
def login_google(browser, auth_text, username, password):
    """login using Google"""
    LOGGER.info('"%s": Login method Google', username)
    auth_text1 = auth_text.split('\t<a href="')
    auth_text2 = auth_text1[1].split('" class="sa')
    time.sleep(1)
    browser.go_to(auth_text2[0])

    LOGGER.info('"%s": Typing in username', username)
    browser.type(username, into='Email')

    LOGGER.info('"%s": pressing next button', username)
    browser.click(css_selector="#next")
    time.sleep(2)

    LOGGER.info('"%s": Typing in password', username)
    browser.type(password, css_selector="input")

    LOGGER.info('"%s": pressing sign in button', username)
    browser.click(css_selector="#submit")
    time.sleep(3)

    # Some why it wont click and login immediately. This seems to work
    time.sleep(1)
    browser.go_to(auth_text2[0])
    time.sleep(1)
    browser.go_to(auth_text2[0])
    time.sleep(1)
    browser.click(
        css_selector="#sa_add2 > div:nth-child(4) > a.sa_link.gogo > div"
    )
    time.sleep(3)
    return browser


# IDK if this is working
def login_vk(browser, auth_text, username, password):
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
def login_facebook(browser, auth_text, username, password):
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
