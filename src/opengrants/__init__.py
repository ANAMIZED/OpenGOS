"""Deprecated package path.

This project was renamed to OpenGOS. Import from `opengos` instead.

    from opengos.server import main
"""

import warnings

warnings.warn(
    "The 'opengrants' package path is deprecated. Use 'opengos' instead.",
    DeprecationWarning,
    stacklevel=2,
)

from opengos import __version__  # noqa: F401,E402
