# Configurave
[![Lint & Test](https://img.shields.io/github/workflow/status/discord-modmail/configurave/Lint%20&%20Test/main?label=Lint+%26+Test&logo=github&style=flat)](https://github.com/discord-modmail/configurave/actions/workflows/lint_test.yml "Lint and Test")
[![Python](https://img.shields.io/static/v1?label=Python&message=3.7+|+3.8+|+3.9&color=blue&logo=Python&style=flat)](https://www.python.org/downloads/ "Python 3.7 | 3.8 | 3.9")
[![Code Style](https://img.shields.io/static/v1?label=Code%20Style&message=black&color=000000&style=flat)](https://github.com/psf/black "The uncompromising python formatter")


Configurave is a one-stop configuration engine that permits writing your configuration as a simple decorated class, and then loading the values from a series of configuration files or providers.

Values loaded from later sources override values provided by earlier sources. Types of the loaded configuration values are checked.

While not currently functional, there are plans and code to write out a default configuration generated directly from the configurave decorated class with .defaults_toml().

This project has undergone _MINIMAL_ testing and work. It is likely very buggy at this time. Stay tuned for more!

Example usage:

```py
from typing import List

from configurave import make_config, ConfigEntry as ce

@make_config(sources=["tests/test-config/readme.toml"])
class MyConfig:
    site_root: str = ce(comment="The root url the site should be mounted on")
    template_root: str = ce(comment="Directory under which templates should be found")
    allowed_hosts: List[str] = ce(
        comment="A comma separated list of hosts that we are permitted to server content to",
        validator=lambda config, value: len(value) > 0,
    )
    token: str = ce(comment="The discord auth token", secret=True)

config = MyConfig()
config.load()

print(config.site_root, config.template_root, config.allowed_hosts[0], sep="\n")

```

This will load from a file that looks like:
```toml
template_root = "./templates"
allowed_hosts = "mydomain.com,example.example,localhost:8080"

[site]
root = "/"
```

or

```env
TEMPLATE_ROOT="./templates"
ALLOWED_HOSTS="mydomain.com,example.example,localhost:8080"
SITE_ROOT="/"
```

and print:
```
/
./templates
["mydomain.com", "example.example", "localhost:8080"]
```
