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
Available login methods: google (supported), vk (may work, never tested), facebook (may work, never tested)
Use username, password, and login method to log in local instance of the authenticator.

RemoteAuthentication connects through a remote API using URL and authentication key.
This is expermental and isn't documentend but I have plans to improve on this in the future.

There is a wrapper available for the following entities:
article, conference, craft, language\_chat, market, overview, perks, profile, resource_state, storage, war, work
For now there is limited documentation how to use the wrapper classes.
Read the files [here](https://github.com/joostsijm/rival_regions_wrapper/tree/dev/src/rival_regions_wrapper/wrapper) to see how they work.

## Examples
Create LocalAuthentication middleware and log in with using environ variables.
```python
import os
from rival_regions_wrapper.middleware import LocalAuthentication

authentication = LocalAuthentication(
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
