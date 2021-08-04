import os

import tomlkit

try:
    from dotenv import load_dotenv
except ImportError:
    # Dotenv is not installed
    load_dotenv: callable = None

from copy import copy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, get_type_hints

try:
    from typing import get_args
except ImportError:
    # Python 3.7
    get_args: callable = None

_UNSET = object()  # sentinel

Source = Union[str, callable]


class Config:
    """The configuration base class for all configurave."""

    _crve_defaults_file: str
    _crve_configs: Dict[str, "ConfigEntry"]
    _crve_sources: List[Source]

    def defaults_toml(self) -> None:
        """Generate a toml string containing comments and default configuration."""
        doc = tomlkit.document()

        # Generate the config class docstring as a file comment. If there isn't one that's fine, just don't
        # add the default Config docstring.
        if self.__doc__ and self.__doc__ != Config.__doc__:
            doc.add(tomlkit.comment(self.__doc__))
        doc.add(tomlkit.comment("This is an autogenerated default configuration file written by Configurave"))

        to_write = list(self._crve_configs.items())
        while to_write:
            name, value = to_write.pop(0)
            default = value.default
            if default is _UNSET:
                continue
            doc.add(name, value.default)
        raise NotImplementedError()
        # return doc.as_string()

    def load(self) -> None:
        """Loads the configuration from all sources."""
        hints = get_type_hints(self.__class__)

        for source in self._crve_sources:
            print("loading config from %r" % source)
            if source == "ENV":
                load_dotenv()
                for name in self._crve_configs:
                    value = os.environ.get(name, None)
                    if value is None:
                        continue

                    if name in hints and callable(hints[name]):
                        hint = hints[name]
                        # Comma separated lists
                        if isinstance(hint, List):
                            if get_args:
                                other_type = get_args(hint).pop()
                            else:
                                # This is nonstandard but supports 3.7
                                other_type = hint.__args__.pop()
                            value = [other_type(i) for i in value.split(",")]
                        else:
                            value = hints[name](value)

                    self._crve_validate_entry(name, value, hints, source)
                    setattr(self, name, value)
                    self._crve_configs[name]._crve_set_from = source

            elif source.endswith(".toml"):
                path = Path(source).resolve()
                if not path.exists():
                    # Don't load missing config files
                    continue
                with path.open("r") as f:
                    config = tomlkit.loads(f.read())
                entries = list(config.items())
                for name, value in entries:
                    print(repr(name), repr(value))
                    if isinstance(value, dict):
                        entries.extend((name + "_" + subname, subvalue) for subname, subvalue in value.items())
                        continue

                    self._crve_validate_entry(name, value, hints, source)
                    setattr(self, name, value)
                    self._crve_configs[name]._crve_set_from = source
            elif callable(source):
                for name, value in source(self):
                    self._crve_validate_entry(name, value, hints, source)
                    setattr(self, name, value)
                    self._crve_configs[name]._crve_set_from = source
            else:
                raise ConfigError("Invalid configuration source %r supplied" % source)

        self.validate_fully_configured()

    def validate_fully_configured(self) -> None:
        """Ensure every config value that needs a value has been set."""
        for name in self._crve_configs:
            if not hasattr(self, name):
                raise ConfigError(
                    "The configuration entry %r needs to be set, but was never set in any of the sources loaded." % name
                )

    def _crve_validate_entry(self, name: str, value: Any, hints: dict, source: Source) -> None:
        """Validate that a given value fits a given configuration entry type and source."""
        if name not in self._crve_configs:
            # TODO: fuzzy match for typos
            raise ConfigError("The configuration entry %r is not an expected configuration value" % name)

        if not isinstance(value, hints[name]):
            raise ConfigError(
                "The configuration entry for %r must be of type %r, not %r with value %r"
                % (name, hints[name], type(value), value)
            )

        if self._crve_configs[name]._crve_set_from == source:
            raise ConfigError("The configuration entry %r has two entries within source %r" % (name, source))


@dataclass
class ConfigEntry:
    """A single configuration entry with metadata."""

    default: Any = _UNSET
    comment: Optional[str] = None
    description: Optional[str] = None
    _crve_set_from: Source = None


class ConfigError(Exception):
    """Custom error type for easy catching."""

    pass


def validate_sources(sources: List[Source]) -> None:
    """Validates that no sources are used without their handler installed."""
    if "ENV" in sources and not load_dotenv:
        raise ConfigError(
            "Environment variables were specified as a source in the configuration setup,"
            " but dotenv is not importable."
        )


def make_config(sources: List[Source]) -> callable:
    """
    Make the given class into a configurave configuration class.

    Converts a provided configuration configuration class into a configuration class
    that supports loading and has attached sources. Note that inheriting classes into
    these configuration classes must be done carefully--configuration parameters are
    per-class, and are not inheritable (make_config must be called on all CE-bearing
    classes).

    :param sources: a list of files or other special sources (such as ENV) to load configuration from
    :return: a decorator that converts the wrapped class
    """

    def wrapper(class_: type) -> type:
        new_attributes = {"_crve_sources": sources, "_crve_configs": {}}
        if Config in class_.__mro__:
            raise ConfigError("Configuration should be created with @make_config, not by subclassing Config.")
        new_class = type(class_.__name__, (Config, class_), new_attributes)
        new_class.__doc__ = class_.__doc__

        validate_sources(sources)

        for name, value in list(class_.__dict__.items()):
            if not isinstance(value, ConfigEntry):
                continue

            new_attributes["_crve_configs"][name] = copy(value)

            # Replace configuration elements with their defaults, or remove if they're unset
            if value.default is _UNSET:
                delattr(class_, name)
            else:
                setattr(new_class, name, value.default)

        return new_class

    return wrapper