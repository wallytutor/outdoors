# -*- coding: utf-8 -*-
""" Generate reports and maps for the Dolomiti Senza Confini.

Based on the following series from https://betterdatascience.com/:
- Part 1: https://rb.gy/543dw
- Part 2: https://rb.gy/siays
- Part 3: https://rb.gy/zzmec
- Part 4: https://rb.gy/ecyvy
- Part 5: https://rb.gy/9kqw4
- Part 6: upcoming

Tiles providers are listed here:
- https://wiki.openstreetmap.org/wiki/Raster_tile_providers
- https://opentopomap.org/
- https://www.cyclosm.org/

Other links:
- https://www.bergsteigen.com/touren/klettersteig/grosse-kinigat-klettersteig/
- https://www.alpenvereinaktiv.com/it/media/29947193/

Goals of the script:
- [ ] Generate a global map with elevation profile for all days.
- [x] Generate individual day maps with elevation profiles.
- [ ] Display waypoints for all refuges and via ferrata limits.
- [ ] Ensure plots are within track boundaries.
- [ ] Create gradient distribution graph.
- [ ]
"""
from pathlib import Path
from branca.colormap import LinearColormap
from folium.plugins import MarkerCluster
from PIL import Image
import json
import io
import webbrowser
import folium
import gpxpy
import numpy as np
import pandas as pd

INTERACTIVE = False

BROWSER = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"

ALT_RNG = (1600, 2600)


def tracks_to_dataframes(paths):
    """ Convert all paths provided into a single table. """
    route_info = []
    track_info = []

    for track_no, track in enumerate(paths):
        track_info.append({

        })

        for segment in track.segments:
            for point in segment.points:
                route_info.append({
                    "track_no": track_no,
                    "latitude": point.latitude,
                    "longitude": point.longitude,
                    "elevation": point.elevation
                })

    return pd.DataFrame(route_info)


def get_bounds(coordinates):
    """ Get SW-NE boundaries from trace coordinates. """
    lat_min = min(coordinates, key=lambda p: p[0])[0]
    lon_min = min(coordinates, key=lambda p: p[1])[1]

    lat_max = max(coordinates, key=lambda p: p[0])[0]
    lon_max = max(coordinates, key=lambda p: p[1])[1]

    bounds = [(lat_min, lon_min), (lat_max, lon_max)]
    return bounds


def map_at_location(location, tiles):
    """ Create map around given location with provided tiles. """
    route_map = folium.Map(
        location=location,
        width="100%",
        height="100%",
        left="0%",
        top="0%",
        position="relative",
        tiles=tiles["URL"],
        attr=tiles["attr"],
        crs="EPSG3857",
        control_scale=True,
        prefer_canvas=False,
        no_touch=True,
        disable_3d=False,
        png_enabled=True,
        zoom_control=False
    )
    return route_map


def add_trace(route_map, coordinates, elevation):
    """ Create an elevation-colored trace. """
    folium.ColorLine(
        positions=coordinates, 
        weight=6,
        colors=elevation,
        colormap=LinearColormap(
            colors=["green", "blue", "red"],
            vmin=ALT_RNG[0],
            vmax=ALT_RNG[1]
        )
    ).add_to(route_map)


def add_gridlines(route_map, bounds, interval=0.002):
    """ Add gridlines to map with given parameters. """
    [(lat_min, lon_min), (lat_max, lon_max)] = bounds
    safety_no = 100

    lat_lines = np.arange(
        lat_min - safety_no * interval,
        lat_max + safety_no * interval,
        interval
    )
    lon_lines = np.arange(
        lon_min - safety_no * interval,
        lon_max + safety_no * interval,
        interval
    )

    for lat in lat_lines:
        folium.PolyLine(
            locations=[[lat, -180], [lat, 180]],
            color="black",
            weight=0.3,
            dash_array="1"
        ).add_to(route_map)

    for lon in lon_lines:
        folium.PolyLine(
            locations=[[-90, lon], [90, lon]],
            color="black",
            weight=0.3,
            dash_array="1"
        ).add_to(route_map)


def add_waypoints(route_map, bounds, waypoints):
    """ Add relevant waypoints to map. """
    cluster = MarkerCluster().add_to(route_map)

    def escoped_waypoints(waypoint):
        return is_waypoint_in(waypoint, bounds)
    
    for point in filter(escoped_waypoints, waypoints):
        popup = ""

        if point["name-it"]:
            popup += f"<b>IT:</b> {point['name-it']}<br>"

        if point["name-de"]:
            popup += f"<b>DE:</b> {point['name-de']}<br>"

        popup = folium.Popup(
            popup,
            min_width=100,
            max_width=300
        )

        folium.Marker(
            point["location"],
            popup=popup
        ).add_to(cluster)


def create_map(coordinates, elevation, waypoints,
               tiles, data_dir, map_name):
    """ Create map with given track trace. """
    bounds = get_bounds(coordinates)
    location = np.mean(np.array(coordinates), axis=0)
    
    route_map = map_at_location(location, tiles)
    route_map.fit_bounds(bounds=bounds)

    add_waypoints(route_map, bounds, waypoints)
    add_trace(route_map, coordinates, elevation)
    add_gridlines(route_map, bounds, interval=0.002)

    saveas = data_dir / f"{map_name}.html"
    route_map.save(saveas)

    if INTERACTIVE:
        webbrowser.get(BROWSER).open(f"file://{saveas}")

    map_to_png(route_map, data_dir / f"{map_name}.png")


def map_to_png(route_map, saveas, time_out=5.0):
    """ Dump map as a PNG file using Selenium. """
    img_data = route_map._to_png(time_out)
    img_data = io.BytesIO(img_data)
    img = Image.open(img_data)
    img.save(saveas)


def is_waypoint_in(waypoint, bounds, tol=0.01):
    """ Check whether waypoint belongs to rectangular region. """
    (lat, lon) = waypoint["location"]
    [(lat_min, lon_min), (lat_max, lon_max)] = bounds

    tests = [
        (lat >= lat_min - tol),
        (lat <= lat_max + tol),
        (lon >= lon_min - tol),
        (lon <= lon_max + tol)
    ]

    return 4 == sum(tests)


def main():
    """ Run map generation for project. """
    # Get path to project data folder.
    data_dir = Path(__file__).resolve().parent / "data"
    project = data_dir / "Dolomiti-Senza-Confini"

    # Get project configuration files.
    gpx_file = project / "2023-05-02-tracks.gpx"
    config_file = project / "config.json"

    # Get GPX data.
    with open(gpx_file, encoding="utf-8") as fp:
        gpx = gpxpy.parse(fp)

    # Get configuration data.
    with open(config_file, encoding="utf-8") as fp:
        config = json.load(fp)

    # Select type of tiles to use.
    tiles = config["tiles"][1]

    # Retrieve waypoints.
    waypoints = config["waypoints"]

    # Set token if required.
    if "token" in tiles["URL"]:
        # Local file holding secrets, do not commit!
        import config_secrets

        tiles["URL"] += config_secrets.mapbox

    # Transform tracks into a table.
    df = tracks_to_dataframes(gpx.tracks)

    # TODO Create some features for reporting.
    # df["elevation_diff"] = df['elevation'].diff() 

    create_map(
        df[["latitude", "longitude"]].to_numpy(),
        df["elevation"],
        waypoints,
        tiles,
        project,
        "map-dolomiti"
    )
    
    # Loop over tracks to create maps.
    for track_no in df["track_no"].unique():
        selection = df.loc[df["track_no"] == track_no]

        create_map(
            selection[["latitude", "longitude"]].to_numpy(), 
            selection["elevation"],
            waypoints,
            tiles,
            project,
            f"map-{track_no}"
        )
 

if __name__ == "__main__":
    main()
