# Configurave
[![Lint & Test](https://img.shields.io/github/workflow/status/discord-modmail/configurave/Lint%20&%20Test/main?label=Lint+%26+Test&logo=github&style=flat)](https://github.com/discord-modmail/configurave/actions/workflows/lint_test.yml "Lint and Test")
[![Codacy Grade](https://img.shields.io/codacy/grade/78be21a49835484595aea556d5920638?logo=codacy&style=flat&label=Code+Quality)](https://www.codacy.com/gh/discord-modmail/configurave/dashboard "Codacy Grade")
[![Python](https://img.shields.io/static/v1?label=Python&message=3.7+|+3.8+|+3.9&color=blue&logo=Python&style=flat)](https://www.python.org/downloads/ "Python 3.7 | 3.8 | 3.9")
[![Code Style](https://img.shields.io/static/v1?label=Code%20Style&message=black&color=000000&style=flat)](https://github.com/psf/black "The uncompromising python formatter")


Configurave is a one-stop configuration engine that permits writing your configuration as a simple decorated class, and then loading the values from a series of configuration files or providers.

Values loaded from later sources override values provided by earlier sources. Types of the loaded configuration values are checked.

While not currently functional, there are plans and code to write out a default configuration generated directly from the configurave decorated class with .defaults_toml().

This project has undergone _MINIMAL_ testing and work. It is likely very buggy at this time. Stay tuned for more!
