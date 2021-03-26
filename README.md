# Rival-Regions-Wrapper
This library will functions as an authenticator an API wrapper for interaction with Rival Regions.
Use at your own risk.

## Install
The following steps can be used to install the package with pip:

```
pip install rival_regions_wrapper
```

The package should be available globaly.

## Testing
This application supports unit tests, these are located in `rival_regions_wrapper/tests/`.
Install required dependencies using `pipenv install --dev`.
After installing you should be able to test the python package with pytest.
Requests are cached for quick testing using VCR.py located at `rival_regions_wrapper/tests/cassettes/`.
If you run in problems with testing you are advised to them run again after remvong the cassettes directory.

The tests read login credentials from the following environment variables:
`LOGIN_METHOD`, `USERNAME`, `PASSWORD`.
You can set those by creating an file named `.env` with te following:

```
LOGIN_METHOD=PLACEHOLDER
USERNAME=PLACEHOLDER
PASSWORD=PLACEHOLDER
```

Replace `PLACEHOLDER` with your credentials.

## Login methods
Currently the working login methods are Google and VK.
If you can help me out and make the other login methods working it would be appreciated. 

login methods:

- google [working]
- vk [working]
- facebook

## Middleware
The API wrapper uses middleware to decide where how to send the request.
Middlewares can also be used to write direct requests to Rival Regions.

Current middleware

### LocalAuthentication
Use username, password, and login method to log in local instance of the authenticator.

### RemoteAuthentication
Connect through a remote API using URL and authentication key.

## Examples
Create local authentication middleware and log in with environ variables
```python
import os
from rival_regions_wrapper import LocalAuthentication

authentication = LocalAuthentication(
  os.environ["RR_USERNAME"],
  os.environ["RR_PASSWORD"],
  os.environ["RR_LOGIN_METHOD"]
)
```

request region page from Rival Regions
```python
region = authentication.get('listed/upgrades/{}'.format(region_id))
```

Example of API wrapper to get oil current available resources from a state
```python
from rival_regions_wrapper import apiWrapper
from rival_regions_wrapper.api_wrapper import ResourceState

api_wrapper = ApiWrapper(authentication)

state = 3382
resource = 'oil'
response = ResourceState(api_wrapper, state).info(resource)
```

For more examples look at the unit tests.

## Contact
* [Discord](https://discord.gg/6fzHtJM)
