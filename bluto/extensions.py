"""Extensions module.
Each extension is initialized in the app factory located in app.py."""

from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension

cache = Cache()
debug_toolbar = DebugToolbarExtension()
