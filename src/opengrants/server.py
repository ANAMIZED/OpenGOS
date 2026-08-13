"""Deprecated compatibility shim. Use opengos.server instead."""

import warnings

warnings.warn(
    "opengrants.server is deprecated. Import from opengos.server instead.",
    DeprecationWarning,
    stacklevel=2,
)

from opengos.server import *  # noqa: F401,F403
from opengos.server import main, mcp
