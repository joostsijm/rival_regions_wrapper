# Rival-Regions-Wrapper
This library will functions as an API wrapper for interaction with Rival Regions.

## Install
The following steps can be used to install the package with pip:

- clone the repository: `git clone git@github.com:jjoo914/rival_regions_wrapper.git`
- use pip to install the package: `pip install rival_regions_wrapper`

The package should be available globaly.

### Pipenv
When you want to add the package to a Pipfile, use the folowing command:
```
pipenv install -e git+https://github.com/jjoo914/rival_regions_wrapper#egg=rival_regions_wrapper
```

## Testing
After installing you should be able to test the python package with pytest.
These are located in `rival_regions_wrapper/tests/`.
Requests are cached for quick testing using VCR.py located at `rival_regions_wrapper/tests/cassettes/`.

## Middleware
The API wrapper uses middleware to decide where how to send the request.
Middlewares can also be used to write direct requests to Rival Regions.

Current middleware

### LocalAuthentication
Use username, password, and login method to log in local instance of the authenticator.

### RemoteAuthentication
Connect through a remote API using URL and authentication key.

## Examples
Create local authentication middleman after that log in with environ variables and request region page from Rival Regions

```python
import os
from rival_regions_wrapper import LocalAuthentication

middleware = LocalAuthentication(
  os.environ["USERNAME"],
  os.environ["PASSWORD"],
  os.environ["LOGIN_METHOD"]
)

region = middleware.get('listed/upgrades/{}'.format(region_id))
```

### Contact
* [Discord](https://discord.gg/6fzHtJM)
