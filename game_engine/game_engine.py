"""Compatibility shim: old module `game_engine.game_engine`.

This module re-exports the actual implementation from `game_engine.engine` to avoid
breaking imports while removing the original module implementation to prevent
conflicts with the `game_engine` package name.
"""

import warnings

warnings.warn(
    "game_engine.game_engine is deprecated — import from game_engine.engine instead",
    DeprecationWarning,
)

# Re-export public symbols from the new module
from .engine import *

# Explicitly declare public API for linters/inspections
__all__ = [name for name in dir() if not name.startswith("_")]

