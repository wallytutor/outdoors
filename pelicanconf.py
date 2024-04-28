###############################################################################
# GENERAL
###############################################################################

AUTHOR = "Walter Dal'Maz Silva"

SITENAME = "Outdoors"

# Keep this empty here to render properly, overriden in publishconf.py.
SITEURL = ""

PATH = "content"

TIMEZONE = "Europe/Paris"

DEFAULT_LANG = "en"

DEFAULT_PAGINATION = 10

RELATIVE_URLS = True

IGNORE_FILES = [".#*", "*.yaml"]

# Static paths are processed after articles, so this must be included to avoid
# failure; otherwise files will get processed and skipped!
ARTICLE_EXCLUDES = ["draft", "media", "venv"]

STATIC_PATHS = ["media"]

###############################################################################
# THEME & ITS SPECIFICS
###############################################################################

THEME = "theme/pelican-twitchy"

SHARE = True

DISPLAY_PAGES_ON_MENU = True

DISPLAY_CATEGORIES_ON_MENU = False

DISPLAY_TAGS_ON_MENU = False

CC_LICENSE = "CC-BY"


###############################################################################
# LINKS
###############################################################################

SOCIAL = (
    ("Strava",    "https://www.strava.com/athletes/109704687"),
    ("Instagram", "https://www.instagram.com/walteriando/"),
)

###############################################################################
# FEED
###############################################################################

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
