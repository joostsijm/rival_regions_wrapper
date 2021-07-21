"""
Rival Regions API methods
"""

import time

from rival_regions_wrapper import LOGGER
from rival_regions_wrapper.cookie_handler import CookieHandler
from rival_regions_wrapper.exceptions import (
    SessionExpireException,
    NoLogginException,
)


def session_handler(func):
    """Handle expired sessions"""

    def wrapper(*args, **kwargs):
        instance = args[0]
        return try_run(instance, func, *args, **kwargs)

    def try_run(instance, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (
            SessionExpireException,
            ConnectionError,
            ConnectionResetError,
        ):
            CookieHandler.remove_cookie(instance.username)
            instance.authenticate()
            return try_run(instance, func, *args, **kwargs)
        except NoLogginException:
            instance.authenticate()
            return try_run(instance, func, *args, **kwargs)

    return wrapper


def check_response(response):
    """Check resonse for authentication"""
    if not isinstance(response, str):
        response = response.text
    if (
        "Session expired, please, reload the page" in response
        or 'window.location="https://rivalregions.com";' in response
    ):
        raise SessionExpireException()


@session_handler
def get(middleware, path, add_var_c=False):
    """Send get request to Rival Regions"""
    if path[0] == "/":
        path = path[1:]

    params = {}
    if add_var_c:
        params["c"] = middleware.authentication_handler.var_c

    LOGGER.info(
        '"%s": GET: "%s" var_c: %s', middleware.username, path, add_var_c
    )
    if middleware.authentication_handler.session:
        response = middleware.authentication_handler.session.get(
            url="https://rivalregions.com/{}".format(path), params=params
        )
        check_response(response)
    else:
        raise NoLogginException()
    return response.text


@session_handler
def post(middleware, path, data=None):
    """Send post request to Rival Regions"""
    if path[0] == "/":
        path = path[1:]
    if not data:
        data = {}
    data["c"] = middleware.authentication_handler.var_c

    LOGGER.info('"%s": POST: "%s"', middleware.username, path)
    if middleware.authentication_handler.session:
        response = middleware.authentication_handler.session.post(
            "https://rivalregions.com/{}".format(path), data=data
        )
        check_response(response)
    else:
        raise NoLogginException()
    return response.text


@session_handler
def conference_message(middleware, conference_id, message):
    """Send conference message"""
    browser = middleware.authentication_handler.get_browser()
    try:
        browser.go_to(
            "https://rivalregions.com/#slide/conference/{}".format(
                conference_id
            )
        )
        browser.refresh()
        time.sleep(2)

        character_count = 0
        tmp_messages = []
        for sentence in message.split("\n"):
            sentence_character_count = 0
            tmp_sentence = []
            for word in sentence.split(" "):
                sentence_character_count += len(word) + 1
                if sentence_character_count >= 899:
                    message = "{}\n{}".format(
                        "\n".join(tmp_messages), " ".join(tmp_sentence)
                    )
                    LOGGER.info(
                        '"%s": CONF "%s": next message length: %s',
                        middleware.username,
                        conference_id,
                        len(message),
                    )
                    browser.type(message, id="message")
                    browser.click(id="chat_send")
                    sentence_character_count = 0
                    tmp_sentence = []
                    character_count = 0
                    tmp_messages = []
                tmp_sentence.append(word)

            sentence = " ".join(tmp_sentence)
            character_count += len(sentence) + 1
            if character_count >= 900:
                message = "\n".join(tmp_messages)
                LOGGER.info(
                    '"%s": CONF "%s": next message length: %s',
                    middleware.username,
                    conference_id,
                    len(message),
                )
                browser.type(message, id="message")
                browser.click(id="chat_send")
                character_count = 0
                tmp_messages = []
            tmp_messages.append(sentence)

        if tmp_messages:
            message = "\n".join(tmp_messages)
            LOGGER.info(
                '"%s": CONF "%s": next message length: %s',
                middleware.username,
                conference_id,
                len(message),
            )
            browser.type(message, id="message")
            browser.click(id="chat_send")

        LOGGER.info(
            '"%s": CONF "%s": finished sending message',
            middleware.username,
            conference_id,
        )
    finally:
        browser.close_current_tab()


@session_handler
def conference_notification(middleware, conference_id, message, sound):
    """Send conference notification"""
    data = {
        "sound": 1 if sound else 0,
        "text": message,
        "c": middleware.authentication_handler.var_c,
    }

    response = middleware.post(
        "https://rivalregions.com/rival/konffcm/{}/".format(conference_id),
        data=data,
    )
    check_response(response)
    LOGGER.info(
        '"%s": CONF: id %s send notification ',
        middleware.username,
        conference_id,
    )
    return response


@session_handler
def conference_change_title(middleware, conference_id, title):
    """Change conference title"""
    data = {
        "t": title,
        "c": middleware.authentication_handler.var_c,
    }
    response = middleware.post(
        "https://rivalregions.com/rival/changename/{}/".format(conference_id),
        data=data,
    )
    check_response(response)
    LOGGER.info(
        '"%s": CONF: id %s changed title', middleware.username, conference_id
    )
    return response


@session_handler
def profile_message(middleware, profile_id, message):
    """send personal message"""
    LOGGER.info('"%s": PM: user id %s', middleware.username, profile_id)
    browser = middleware.authentication_handler.get_browser()
    try:
        browser.go_to(
            "https://rivalregions.com/#messages/{}".format(profile_id)
        )
        browser.refresh()
        time.sleep(2)
        browser.type(message, id="message")
        browser.click(id="chat_send")
        LOGGER.info(
            '"%s:" PM: user id %s, finished sending message',
            middleware.username,
            profile_id,
        )
    finally:
        browser.close_current_tab()


@session_handler
def language_message(middleware, language, message):
    """Send message in language chat"""
    browser = middleware.authentication_handler.get_browser()
    try:
        browser.go_to(
            "https://rivalregions.com/#slide/chat/lang_{}".format(language)
        )
        browser.refresh()
        time.sleep(2)
        browser.type(message, id="message")
        browser.click(id="chat_send")

        LOGGER.info(
            '"%s": CHAT: language %s, finished sending message',
            middleware.username,
            language,
        )
    finally:
        browser.close_current_tab()
