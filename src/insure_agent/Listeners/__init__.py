# This file makes the 'Listeners' directory a Python package.
# It also ensures that listener instances are loaded and registered when the package is imported.

from .custom_event import logging_custom_listener

# Optionally, you can define __all__ if you want to control what 'from Listeners import *' imports
__all__ = ['logging_custom_listener']

print(f"[{__name__}] Listeners package initialized, logging_custom_listener imported.")
