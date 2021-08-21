import pytest

from configurave import ConfigEntry as ce
from configurave import ConfigError, make_config

"""
Apply basic tests to configurave config loading.
"""


@pytest.mark.dependency(name="load_dotenv")
def test_validate_sources_env():
    """Test env sources are validated properly."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        pytest.skip("dotenv not installed")

    from configurave import validate_sources

    validate_sources(["ENV"])


def test_validate_sources_env_dotenv_not_installed():
    """Test env source errors properly when dotenv is not installed."""
    import configurave
    from configurave import load_dotenv, validate_sources

    if load_dotenv is not None:
        pytest.skip("dotenv is installed")

    with pytest.raises(ConfigError):
        validate_sources(["ENV"])


def test_everything():
    """We can create and load a configuration from our test config folder."""
    # TODO: split this up and write better tests

    @make_config(
        sources=[  # in order of priority
            "tests/test-config/config.toml",
            # "ENV",  # Temporarily disabled until we get optional dotenv test up and running
        ]
    )
    class Config:
        """The test configuration for configurave."""

        root_url: str = ce(
            comment="The root url configuration for the application",
            description="A long ass multiline description goes here about all the options"
            " you could potentially decide upon using.",
        )

    c = Config()
    c.load()

    assert "root_url" in str(c._crve_configs)
    assert c.root_url == "test url"

    # print("Defaults toml file:\n" + c.generate_defaults())


@pytest.mark.xfail(reason="Not finished.")
@pytest.mark.dependency(depends=["load_dotenv"])
def test_missing_config():
    """Test an error is raised when a file does not exist."""

    @make_config(
        sources=[  # in order of priority
            "tests/test-config/fake-config.toml",
        ]
    )
    class Config:
        """The test configuration for configurave."""

        root_url: str = ce(
            comment="The root url configuration for the application",
            description="A long ass multiline description goes here about all the options"
            " you could potentially decide upon using.",
        )

    c = Config()
    c.load()
