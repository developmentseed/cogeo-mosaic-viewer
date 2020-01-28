# cogeo-mosaic-viewer

Visualize [Mosaic](https://github.com/developmentseed/mosaicjson-spec) of Cloud Optimized GeoTIFF in browser.

![](https://user-images.githubusercontent.com/10407788/70332350-62d62980-180f-11ea-9527-9eaecdbcdbc5.png)

### Install

```bash
# python-vtzero will only compile with Cython < 0.29
$ pip install cython==0.28
$ pip install git+https://github.com/developmentseed/cogeo-mosaic-viewer.git
```

##### CLI
```bash 
$ cogeo-mosaic viewer --help                 
Usage: cogeo-mosaic viewer [OPTIONS] MOSAIC_PATH

  cogeo-mosaic Viewer.

Options:
  --style [satellite|basic]  Mapbox basemap
  --port INTEGER             Webserver port (default: 8080)
  --host TEXT                Webserver host url (default: 127.0.0.1)
  --mapbox-token TOKEN       Mapbox token
  --footprint                Visualize Mosaic Footprint
  --help                     Show this message and exit.
```

Create mosaic-json file (see [cogeo-mosaic](https://github.com/developmentseed/cogeo-mosaic))

