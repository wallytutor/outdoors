# -*- coding: utf-8 -*-
from folium.plugins import MarkerCluster
from gpxtohtml import OPENTOPOMAP
from gpxtohtml import GpxToHtml

# Rough bounds of France.
bounds = [(44.0, 2.0), (50.0, 7.0)]

# This is Paris:
location = [48.8575, 2.3514]

waypoints = [
    {
        "name": "Chamrousse (Lacs Robert)",
        "url": "https://www.chamrousse.com/plan-via-ferratas.html",
        "location": [45.130000, 5.910000]
    },
    {
        "name": "Les Prises de la Bastille",
        "url": "https://www.grenoble.fr/2882-via-ferrata-et-escalade-a-la-bastille.htm",
        "location": [45.19468, 5.71966]
    },
    {
        "name": "Mines du Grand Clôt",
        "url": "https://www.oisans.com/equipement/via-ferrata-des-mines-du-grand-clot/",
        "location": [45.0423567578637, 6.26036167144775]
    }
]

tiles = OPENTOPOMAP

opts = dict(
    width         = "100%",
    height        = "100%",
    left          = "0%",
    top           = "0%",
    position      = "relative",
    crs           = "EPSG3857",
    control_scale = True,
    prefer_canvas = False,
    no_touch      = True,
    disable_3d    = False,
    png_enabled   = True,
    zoom_control  = True
)

route_map = GpxToHtml.map_at_location(location, tiles, opts=opts)
route_map.fit_bounds(bounds)

cluster = MarkerCluster().add_to(route_map)

for point in waypoints:
    GpxToHtml.feed_waypoint(cluster, point, bounds)

route_map.save("content/media/via-ferrata/index.html")
