"""setup: cogeo-mosaic-viewer"""

from setuptools import setup, find_packages

# Runtime requirements.
inst_reqs = ["rio-viz", "cogeo-mosaic"]
extra_reqs = {}

setup(
    name="cogeo-mosaic-viewer",
    version="0.0.1",
    python_requires=">=3",
    description=u"Visualize Cloud Optimized GeoTIFF Mosaics in browser",
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    keywords="COG COGEO Rasterio GIS MVT",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    include_package_data=True,
    zip_safe=False,
    license="MIT",
    install_requires=inst_reqs,
    extras_require=extra_reqs,
    entry_points="""
      [cogeo_mosaic.plugins]
      viewer=cogeo_mosaic_viewer.scripts.cli:viewer
      """,
)
