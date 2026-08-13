"""Deprecated. Use: python -m opengos"""

import warnings

warnings.warn(
    "python -m opengrants is deprecated. Use python -m opengos",
    DeprecationWarning,
    stacklevel=2,
)

from opengos.server import main

if __name__ == "__main__":
    main()
