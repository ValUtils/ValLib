# ValLib

[![PyPI - Version](https://img.shields.io/pypi/v/ValLib?label=ValLib)](https://pypi.org/project/ValLib/)
![GitHub deployments](https://img.shields.io/github/deployments/ValUtils/ValLib/deploy?label=deploy)
![GitHub](https://img.shields.io/github/license/ValUtils/ValLib)

A Python authentication module for the RiotGames API, and basic endpoint provider for Valorant.

## Features

- Full auth flow
- Request helpers
- Basic endpoints for Valorant
- Captcha "bypass" without using external services
- Ability to use external Captcha solvers

## Installation

The prefered method of instaltion is through `pip` but if you know better use the package manager that you want.

```sh
pip install ValLib
```

## Reference

### Basic structure

ValLib contains this basic building blocks:

- `User` a dataclass containing username and password
- `Auth` a dataclass containing ever auth param
- `AuthException` a exception class for **only** when the auth goes wrong because of Riot

And the following methdos:

- `authenticate` to auth with username+password
- `cookie_token` to auth with cookies instead of username+password
- `make_headers` to convert `Auth` into headers for making requests

### Ussage

#### Without API helper

```python
import ValLib
import requests

user = ValLib.User("Test", "TestPassword")
auth = ValLib.authenticate(user)
headers = ValLib.make_headers(auth)
data = requests.get("https://auth.riotgames.com/userinfo", headers=headers)
print(data.json())
```

#### With API helper

```python
import ValLib
from ValLib.api import get_api, put_api, post_api

user = ValLib.User("Test", "TestPassword")
auth = ValLib.authenticate(user)
data = get_api("https://auth.riotgames.com/userinfo", auth)
print(data.json())
```

### Regions and Shards

Getting the region and the shard is often one of the most complicated of managing the API.
So for that we have the `get_region` and `get_shard` methods inside `ValLib.api` and the `ExtraAuth` dataclass inside `ValLib.structs`.

```python
import ValLib
from ValLib.api import get_region, get_shard
from ValLib.structs import ExtraAuth

user = ValLib.User("Test", "TestPassword")
auth = ValLib.authenticate(user)
region = get_region(auth)
shard = get_shard(region)
extra = ExtraAuth(user.username, region, auth)
```

With this new instance of `ExtraAuth` we can use the custom API methods that require it of `ValLib.api`.

### Custom methods

Inside `ValLib.api` there are this customs methods:

- `get_preference` to fetch the in-game settings for Valorant
- `set_preference` to set the in-game settings for Valorant
- `get_load_out` to get the loadout (cosmetics + incognito) for Valorant
- `set_load_out` to set the loadout (cosmetics + incognito) for Valorant
- `get_session` to grab information about the current Valorant session

### Custom Captcha provider

If you need to make automatic auth or just need another way of dealing with captcha you can make your own `CaptchaSolver` class. Here is an example how to do so:

```python
import ValLib
import requests
from ValLib.captcha import CaptchaSolver, set_solver

class DumbCaptcha(CaptchaSolver):
    def token(self, rqdata, site_key):
        r = requests.get(
            "https://myapi.com",
            json={"rqdata": rqdata, "siteKey": site_key}
        )
        return r.text()

set_solver(DumbCaptcha())
user = ValLib.User("MyUser", "MyPass")
auth = ValLib.authenticate(user) # Will use api for captcha solving
```

**DISCLAMER**: most captcha solving APIs exploit people to solve captchas so I'd recommend agaisnt using them but it's at your own risk.

## Roadmap

- [ ] Async
- [ ] More endpoints
- [ ] Better documentation
- [ ] Better exports

## Running Tests

Tests need to be run in a development enviroment with GUI, a navigator, `pytest` and filling this enviroment variables.

```sh
USERNAME="TestUser"
PASSWORD="TestPassword"
```

And then running `pytest`.

## Acknowledgements

- Thanks to [Valorant-API](https://valorant-api.com/) and their mantainers
- Thanks to [Hawolt](https://github.com/hawolt) for discovering the Captcha solver
- Thanks to [Techdoodle](https://github.com/techchrism) for his API docs
- Thanks to the Valorant App Developers discord
