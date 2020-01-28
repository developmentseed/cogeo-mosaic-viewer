"""cogeo_mosaic_viewer.raster: raster tiles object."""

from typing import Tuple

import numpy
import mercantile
import rasterio
from rio_tiler.main import tile as cogeoTiler
from rio_tiler_mosaic.mosaic import mosaic_tiler
from rio_tiler_mosaic.methods import defaults

from rio_viz import raster
from cogeo_mosaic import utils


def get_layer_names(src_dst):
    """Get Rasterio dataset band names."""

    def _get_name(ix):
        name = src_dst.descriptions[ix - 1]
        if not name:
            name = f"band{ix}"
        return name

    return [_get_name(ix) for ix in src_dst.indexes]


class MosaicRasterTiles(raster.RasterTiles):
    """Raster tiles object."""

    def __init__(self, mosaic_path: str):
        """Initialize MosaicRasterTiles object."""
        self.path = mosaic_path
        self.mosaic = utils.fetch_mosaic_definition(self.path)
        self.bounds = self.mosaic["bounds"]
        self.center = [
            (self.bounds[0] + self.bounds[2]) / 2,
            (self.bounds[1] + self.bounds[3]) / 2,
        ]
        self.minzoom = self.mosaic["minzoom"]
        self.maxzoom = self.mosaic["maxzoom"]

        # read layernames from the first file
        quadkeys = list(self.mosaic["tiles"].keys())
        src_path = self.mosaic["tiles"][quadkeys[0]][0]
        with rasterio.open(src_path) as src_dst:
            self.band_descriptions = get_layer_names(src_dst)
            self.data_type = src_dst.dtypes[0]

    def read_tile(
        self,
        z: int,
        x: int,
        y: int,
        tilesize: int = 256,
        indexes: Tuple[int] = None,
        resampling_method: str = "bilinear",
    ) -> [numpy.ndarray, numpy.ndarray]:
        """Read raster tile data and mask."""
        assets = utils.get_assets(self.mosaic, x, y, z)
        return mosaic_tiler(
            assets,
            x,
            y,
            z,
            cogeoTiler,
            indexes=indexes,
            tilesize=tilesize,
            pixel_selection=defaults.FirstMethod(),
            resampling_method=resampling_method,
        )

    def point(self, coordinates: Tuple[float, float]) -> dict:
        """Read point value."""
        min_zoom = self.mosaic["minzoom"]
        quadkey_zoom = self.mosaic.get("quadkey_zoom", min_zoom)  # 0.0.2
        tile = mercantile.tile(coordinates[0], coordinates[1], quadkey_zoom)
        assets = utils.get_assets(self.mosaic, tile.x, tile.y, tile.z)
        results = utils.get_point_values(assets, coordinates[0], coordinates[1])

        return {"coordinates": coordinates, "value": results[0]["values"]}

    def metadata(self) -> dict:
        """Get Raster metadata."""
        info = {
            "bounds": {"value": self.bounds, "crs": "epsg:4326"},
            "minzoom": self.minzoom,
            "maxzoom": self.maxzoom,
        }
        info["dtype"] = self.data_type
        info["band_descriptions"] = [(b, b) for b in self.band_descriptions]
        return info

    def geojson(self) -> dict:
        """Get Raster metadata."""
        return {
            "type": "FeatureCollection",
            "features": [
                mercantile.feature(
                    mercantile.quadkey_to_tile(qk), props=dict(files=files)
                )
                for qk, files in self.mosaic["tiles"].items()
            ],
        }
