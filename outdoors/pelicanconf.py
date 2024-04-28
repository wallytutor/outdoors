AUTHOR = "Walter Dal'Maz Silva"

SITENAME = "Outdoors"

# SITEURL = ""
# SITEURL = "https://wallytutor.github.io/outdoors/"

PATH = "content"

TIMEZONE = "Europe/Paris"

DEFAULT_LANG = "English"

THEME = "notmyidea"

GITHUB_URL = "https://github.com/wallytutor/outdoors"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Strava",    "https://www.strava.com/athletes/109704687"),
    ("Instagram", "https://www.instagram.com/walteriando/"),
)

# Social widget
# SOCIAL = (
#     ("Strava",    "https://www.strava.com/athletes/109704687"),
#     ("Instagram", "https://www.instagram.com/walteriando/"),
# )

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

# List of patters for files to be excluded.
IGNORE_FILES = [".#*", "*.yaml"]

# Static paths are processed after articles, so this must be included to avoid
# failure; otherwise files will get processed and skipped!
ARTICLE_EXCLUDES = ["media"]

# Paths to be copied to final outputs.
STATIC_PATHS     = ["media"]

