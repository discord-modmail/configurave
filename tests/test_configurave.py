import unittest

from configurave import ConfigEntry as ce
from configurave import make_config

"""
Apply basic tests to configurave config loading.
"""


class TestConfigurave(unittest.TestCase):
    """General tests."""

    def test_everything(self):
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

        self.assertIn("root_url", str(c._crve_configs))
        self.assertEqual(c.root_url, "test url")

        # print("Defaults toml file:\n" + c.generate_defaults())
