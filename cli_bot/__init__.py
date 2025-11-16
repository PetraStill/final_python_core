"""Package metadata and shortcuts for the CLI bot."""

__all__ = ["main", "__version__"]

__version__ = "0.1.0"

from .main import main  # noqa: E402  (import after defining __version__)

