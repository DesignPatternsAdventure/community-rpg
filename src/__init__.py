"""community-rpg source code."""

from warnings import filterwarnings

from beartype.roar import BeartypeDecorHintPep585DeprecationWarning

__version__ = "0.1.0"
__pkg_name__ = "community_rpg"

# FYI: https://github.com/beartype/beartype#are-we-on-the-worst-timeline
filterwarnings("ignore", category=BeartypeDecorHintPep585DeprecationWarning)
