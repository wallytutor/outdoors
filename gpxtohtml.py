# -*- coding: utf-8 -*-
from branca.colormap import LinearColormap
from folium.plugins import MarkerCluster
from pathlib import Path
from PIL import Image
import folium
import gpxpy
import io
import numpy as np
import pandas as pd
import yaml


class Tiles:
    """ Representation of tiles for map rendering. """
    def __init__(self, url, attr) -> None:
        self._url = url
        self._attribution = attr

    @property
    def url(self):
        """ Provides access to attribute. """
        return self._url

    @property
    def attribution(self):
        """ Provides access to attribute. """
        return self._attribution
    

class Waypoint:
    """ Representation of a waypoint for tagging the map. """
    def __init__(self, name, location, url) -> None:
        self._name = name
        self._location = location
        self._url = url

    def isinside(self, bounds, tol = 0.01):
        """ Check whether waypoint belongs to rectangular region. """
        (lat, lon) = self._location
        [(lat_min, lon_min), (lat_max, lon_max)] = bounds

        tests = [
            (lat >= lat_min - tol),
            (lat <= lat_max + tol),
            (lon >= lon_min - tol),
            (lon <= lon_max + tol)
        ]

        return all(tests)

    @property
    def name(self):
        """ Provides access to attribute. """
        return self._name
    
    @property
    def location(self):
        """ Provides access to attribute. """
        return self._location
    
    @property
    def url(self):
        """ Provides access to attribute. """
        return self._url

    @property
    def link(self):
        """ Provides access to attribute. """
        return f"<a href=\"{self._url}\" target=\"_blank\">{self._name}</a>"


class GpxToHtml:
    """ Convert a GPX track to an embedable HTML file. """
    def __init__(self, trace_path, force=False, dump_png=False):
        trace_conf = trace.parent / "track.yaml"
        trace_imag = trace.parent / "track.png"
        trace_html = trace.parent / "index.html"

        if trace_html.exists() and not force:
            print(f"Delete {trace_html} and run a new workflow")
        else:
            self._gpx = self.loadgpx(trace_path)
            self._gpc = self.loadcnf(trace_conf)
            self._tab = self.tracks2df(self._gpx.tracks)

            tiles = Tiles(**self._gpc["tiles"])
            grid_interval = self._gpc["grid_interval"]
            
            coordinates = self._tab[["latitude", "longitude"]].to_numpy()
            elevation = self._tab["elevation"].to_numpy()

            bounds = self.get_bounds(coordinates)
            location = np.mean(np.array(coordinates), axis=0)
            
            self._map = self.map_at_location(location, tiles)
            self._map.fit_bounds(bounds=bounds)

            if waypoints := self._gpc.get("waypoints", None):
                self.add_waypoints(bounds, waypoints)

            self.add_trace(coordinates, elevation)
            self.add_gridlines(bounds, grid_interval)
            self._map.save(trace_html)

            if dump_png:
                self.dump_png(trace_imag)

    @staticmethod
    def loadgpx(tracepath: Path) -> gpxpy.gpx.GPX:
        """ Load GPX file from provided path. """
        with open(tracepath, encoding="utf-8") as fp:
            gpx = gpxpy.parse(fp)
        return gpx

    @staticmethod
    def loadcnf(cnfpath: Path) -> dict:
        """ Load configuration file from provided path. """
        with open(cnfpath, encoding="utf-8") as fp:
            cnf = yaml.safe_load(fp)
        return cnf

    @staticmethod
    def segments2df(track_no: int, segments: list) -> pd.DataFrame:
        """ Convert segments to data-frame. """
        route_info = []

        for segment in segments:
            for point in segment.points:
                route_info.append({
                    "track_no": track_no,
                    "latitude": point.latitude,
                    "longitude": point.longitude,
                    "elevation": point.elevation
                })

        return pd.DataFrame(route_info)

    @staticmethod
    def tracks2df(paths: list):
        """ Convert all paths provided into a single table. """
        routes = []

        for track_no, track in enumerate(paths):
            # TODO: get metadata with something as track_info.append({})
            routes.append(GpxToHtml.segments2df(track_no, track.segments))

        return pd.concat(routes)

    @staticmethod
    def get_bounds(coordinates):
        """ Get SW-NE boundaries from trace coordinates. """
        lat_min = min(coordinates, key=lambda p: p[0])[0]
        lon_min = min(coordinates, key=lambda p: p[1])[1]

        lat_max = max(coordinates, key=lambda p: p[0])[0]
        lon_max = max(coordinates, key=lambda p: p[1])[1]

        bounds = [(lat_min, lon_min), (lat_max, lon_max)]
        return bounds

    @staticmethod
    def map_at_location(location, tiles, opts=None):
        """ Create map around given location with provided tiles. """
        opts = opts if opts is not None else dict(
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
            zoom_control  = False
        )

        route_map = folium.Map(location = location, tiles = tiles.url,
                               attr = tiles.attribution, **opts)

        return route_map

    @staticmethod
    def feed_waypoint(cluster, point, bounds):
        """ Feed a single waypoint to map. """
        wp = Waypoint(**point)

        if not wp.isinside(bounds):
            return

        popup = folium.Popup(wp.link, min_width=100, max_width=300)
        folium.Marker(wp.location, popup=popup).add_to(cluster)

    def add_trace(self, coordinates, elevation):
        """ Create an elevation-colored trace. """
        folium.ColorLine(
            positions  = coordinates, 
            weight     = 6,
            colors     = elevation,
            colormap   = LinearColormap(
                colors = ["green", "blue", "red"],
                vmin   = self._gpc["altitude_range"][0],
                vmax   = self._gpc["altitude_range"][1]
            )
        ).add_to(self._map)

    def add_waypoints(self, bounds, waypoints):
        """ Add relevant waypoints to map. """
        cluster = MarkerCluster().add_to(self._map)

        for point in waypoints:
            self.feed_waypoint(cluster, point, bounds)

    def add_gridlines(self, bounds, interval):
        """ Add gridlines to map with given parameters. """
        [(lat_min, lon_min), (lat_max, lon_max)] = bounds

        lat_lines = np.arange(
            lat_min - interval,
            lat_max + interval,
            interval
        )

        lon_lines = np.arange(
            lon_min - interval,
            lon_max + interval,
            interval
        )

        for lat in lat_lines:
            folium.PolyLine(
                locations  = [[lat, -180], [lat, 180]],
                color      = "black",
                weight     = 0.3,
                dash_array = "1"
            ).add_to(self._map)

        for lon in lon_lines:
            folium.PolyLine(
                locations  = [[-90, lon], [90, lon]],
                color      = "black",
                weight     = 0.3,
                dash_array = "1"
            ).add_to(self._map)

    def dump_png(self, saveas, time_out=5.0):
        """ Dump map as a PNG file using Selenium. """
        img_data = self._map._to_png(time_out)
        img_data = io.BytesIO(img_data)
        img = Image.open(img_data)
        img.save(saveas)


OPENSTREETMAPFR = Tiles(
    url  = "https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png",
    attr = "&copy; OpenStreetMap France"
)

OPENTOPOMAP = Tiles(
    url  = "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
    attr = "&copy; OpenTopoMap"
)

CYCLOSM = Tiles(
    url  = "https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png",
    attr = "&copy; CyclOSM"
)

MTBMAP = Tiles(
    url  = "http://tile.mtbmap.cz/mtbmap_tiles/{z}/{x}/{y}.png",
    attr = "&copy; MtbMap"
)


if __name__ == "__main__":
    project = Path(__file__).resolve().parent / "content"

    for trace in (project / "media").glob("**/*.gpx"):
        print(f"Woking on trace {trace}")
        GpxToHtml(trace, force=False)
