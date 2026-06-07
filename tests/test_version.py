import re

import squidink


def test_version_is_semver():
    assert re.fullmatch(r"\d+\.\d+\.\d+", squidink.__version__)
