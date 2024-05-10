# -*- coding: utf-8 -*-
from folium.plugins import MarkerCluster
from gpxtohtml import GpxToHtml
from gpxtohtml import Waypoint
import gpxtohtml
import numpy as np
import yaml

cnfpath = "content/media/via-ferrata/config.yaml"

with open(cnfpath, encoding="utf-8") as fp:
    cnf = yaml.safe_load(fp)

waypoints = cnf["waypoints"]

coordinates = Waypoint.get_coordinates(waypoints)

bounds = GpxToHtml.get_bounds(coordinates)

location = np.mean(coordinates, axis=0)

tiles = gpxtohtml.OPENTOPOMAP

opts = dict(
    width         = "100%",
    height        = "100%",
    left          = "0%",
    top           = "0%",
    min_zoom      = 5,
    max_zoom      = 18,
    position      = "relative",
    crs           = "EPSG3857",
    control_scale = True,
    prefer_canvas = False,
    no_touch      = True,
    disable_3d    = False,
    png_enabled   = True,
    zoom_control  = True,
)

route_map = GpxToHtml.map_at_location(location, tiles, opts=opts)
route_map.fit_bounds(bounds)

cluster = MarkerCluster().add_to(route_map)

for point in waypoints:
    GpxToHtml.feed_waypoint(cluster, point, bounds)

route_map.save("content/media/via-ferrata/index.html")
