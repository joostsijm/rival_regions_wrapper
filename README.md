# Rival-Regions-Wrapper
This library functions as an authenticator and API wrapper for interaction with Rival Regions.
Use at your own risk.

## Install
This package is available on the Python Package Index (PyPi) under the name [rival-regions-wrapper](https://pypi.org/project/rival-regions-wrapper/).
Use the following command to install the package globaly using pip:

```
pip install rival_regions_wrapper
```

When running on local authentication it is also required to have [ChromeDriver](https://sites.google.com/chromium.org/driver/) installed.
This to automate browser actions to account login, private-, conference-, and language chat messages.

Alternative when you want to use the development version you can clone the repository localy.
Check out the dev branch, then run `pip install -e .` inside the directory to install the package globaly.
It is then possible to edit the source code for development and testing. 

## Usage 
Authentication is done through a middleware module that determines how to send the request.
The middleware can also be used to write direct requests to Rival Regions in case the wrapper classes dont suffice.
If you are unsure middleware to use, then it is advised to implement LocalAuthentication.

LocalAuthentication is used to login in directly into Rival Regions using supported login methods.
When running into issues with login then I would appreciate if you could help me resolve the issue. 
Available login methods: Google (supported), vk (may work, never tested), facebook (may work, never tested)
Use username, password, and login method to log in local instance of the authenticator.

RemoteAuthentication connects through a remote API using URL and authentication key.
This is expermental and isn't documentend but I have plans to improve on this in the future.

There is a wrapper available for the following entities:
article, conference, craft, language\_chat, market, overview, perks, profile, resource_state, storage, war, work
For now there is limited documentation how to use the wrapper classes.
Read the files [here](https://github.com/joostsijm/rival_regions_wrapper/tree/dev/src/rival_regions_wrapper/wrapper) to see how they work.

## Problems
### This browser or app may not be secure
Probably the most common problems you may encounter will be about authentication your account.
In some cases for Google accounts while logging in the browser automation tools are detected.
After submitting the google username it gets a prompt that says: "This browser or app may not be secure".
To resolve this problem it is required to run the library with the `show_window` option, when you start the library it will show a Google Chrome window.
This is required because you will have to fill in your loggin credentials by yourself.
It is only required once, because from then on your Google authentication is saved in the Chrome profile.

1. To start the library with `show_window` option, add `True` to the initializing of the LocalAuthentication class, like this: `LocalAuthentication(True)`.
2. Start your application, you will see a Google Chrome window what fills in your username.
4. After submitting your username you see the error message, and a new tab opens.
5. In the new tab log into your Google account.
6. After sucessfully loggin in wait until Google Chrome closes.

From now on you should be able to use your Google account with the library without a problem.
You can disable the library show\_window option by removing `True` when calling the `LocalAuthentication`.

When you face this issue on a headless server it can be solved by copying the Google Chrome profile from your local machine to the server.
The profile is located in the following directory on Linux: `~/.local/share/rival_regions_wrapper/chrome/`.

### Captcha
When loggin in to your Google account makes you fill out a captcha you can use [anti-captcha](https://anti-captcha.com/) service to circumvent them. 
Put the key into the LocalAuthenticator after the show\_window option, like this: `LocalAuthentication(False, <ant_captcha_key>)`.

## Examples
Create LocalAuthentication middleware and log in using environ variables.
```python
import os
from rival_regions_wrapper.middleware import LocalAuthentication

authentication = LocalAuthentication()
authentication.set_credentials(
  os.environ["USERNAME"],
  os.environ["PASSWORD"],
  os.environ["LOGIN_METHOD"]
)
```

request region page from Rival Regions.
```python
region = authentication.get('listed/upgrades/{}'.format(region_id))
```

Example of API wrapper to get oil current available resources from a state.
```python
from rival_regions_wrapper.wrapper import ResourceState

state = 3382
resource = 'oil'
response = ResourceState(authentication, state).info(resource)
```

For more examples look at the unit tests.

## Testing
This libary supports unit tests, these can be found in `rival_regions_wrapper/tests/`.
To run them besides, Pip it is also required to install [Pipenv](https://pypi.org/project/pipenv/).
Clone the repository localy, then intall required development dependencies using `pipenv install --dev`.
After installing these packages, you are able to run the tests with the `pytest` command.

Requests are cached for quick testing using VCR.py located at `rival_regions_wrapper/tests/cassettes/`.
If you run in problems with testing you are advised to them run again after removing the cassettes directory.
Use the parameter `--disable-vcr` to disable VCR temporaly when running Pytest.

The tests read login credentials and other information from the following environment variables:
`USERNAME`, `PASSWORD`, and `LOGIN_METHOD`.
You can set those variables by copying `example.env` to .env`.
Replace `PLACEHOLDER` with your credentials.

Required environ variables:
```
USERNAME=PLACEHOLDER
PASSWORD=PLACEHOLDER
LOGIN_METHOD=PLACEHOLDER
```

There are several optional environ variables, as you can see here with some example value. 
```
CAPTCHA_KEY=59f34d451658f55a517eb1395df52331f
CONFERENCE_ID=439289
CONFERENCE_TITLE=test
LANGUAGE_CHAT=da
PERK=strenght
PERK_UPGRADE_TYPE=gold
CRAFT_ITEM=energy_drink
CRAFT_AMOUNT=10
PROFILE_ID=2000340574
MESSAGE=test
```

In case you want to use the anti-caption service you can fill in the key in `CAPTCHA_KEY`.
Other variables are required to run test that are skipped by default.
These test are skipped because the test sends out a request that makes change to Rival Regions, like sending messages, or crafting items.
You can run those these test by changing the appropiate environ variable and adding the `--no-skip` parameter.
When using this parameter it is advised to specify which test to run.
This can be done with the `-k` parameter, for example `pytest -k profile_message --disable-vcr --no-skips`.
To get a more verbose output from Pytest, use the `-v` parameter.
To see log output of library use the `-s` parameter.

## Contact
* [Discord](https://discord.gg/6fzHtJM)
