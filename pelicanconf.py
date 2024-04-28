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

# THEME = "../pelican-themes/aboutwilson"
# THEME = "../pelican-themes/bold"
# THEME = "../pelican-themes/BT3-Flat"
# THEME = "../pelican-themes/built-texts"
# THEME = "../pelican-themes/Casper2Pelican"
# THEME = "../pelican-themes/cid"
# THEME = "../pelican-themes/eevee"
# THEME = "../pelican-themes/elegant"
# THEME = "../pelican-themes/Flex"
# THEME = "../pelican-themes/foundation-default-colours"
# THEME = "../pelican-themes/gum"
# THEME = "../pelican-themes/hyde"
# THEME = "../pelican-themes/medius"
# THEME = "../pelican-themes/mg"
# THEME = "../pelican-themes/MinimalXY"
# THEME = "../pelican-themes/Peli-Kiera"
# THEME = "../pelican-themes/tuxlite_zf"
THEME = "theme/zurb-F5-basic"

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
