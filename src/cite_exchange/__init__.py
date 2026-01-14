from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("cite_exchange") # 'name' of package from pyproject.toml
except PackageNotFoundError:
    # Package is not installed (e.g., running from a local script)
    __version__ = "unknown"

from .blocks import CexBlock, labels, valid_label

__all__ = ["CexBlock", "labels", "valid_label"]


