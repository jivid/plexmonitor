import importlib
import os

settings_path = os.getenv('PLEXMONITOR_SETTINGS')
if settings_path:
    settings = importlib.import_module(settings_path)
else:
    settings = importlib.import_module('plexmonitor.settings.github')

globals().update(settings.__dict__)
