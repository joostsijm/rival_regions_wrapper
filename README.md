# Rival-Regions-Wrapper
This library will functions as an API wrapper for interaction with Rival Regions.

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
