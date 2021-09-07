import pytest

from configurave import ConfigEntry as ce
from configurave import ConfigError, make_config


def test_toml_dupe_keys():
    """Test an error is raised when a file does not exist."""
    import atoml

    @make_config(
        sources=[  # in order of priority
            "tests/test-config/invalid-toml-tests/dupe-keys.toml",
        ]
    )
    class Config:
        """The test configuration for configurave."""

        test_abc: str = ce(
            comment="The root url configuration for the application",
            description="A long ass multiline description goes here about all the options"
            " you could potentially decide upon using.",
        )

    c = Config(load_now=False)
    with pytest.raises(atoml.exceptions.KeyAlreadyPresent):
        c.load()
