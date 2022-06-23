# -*- coding: utf-8 -*-
"""
Run setup - download needed LiDAR files
"""

import json
import pathlib
import geoapis
import geoapis.lidar
import geopandas


def main():
    """ The setup.main function updates the paths in the instruction file based
    on the run location, and downloads all LiDAR data required for the later
    GeoFabrics processing steps. """

    print("Run setup!")

    ## Define paths
    # note if calling python direct use: 'base_path = pathlib.Path().cwd()'
    base_path = pathlib.Path().cwd().parent.parent.parent
    cache_path = base_path / "data"

    ## Read in the instruction file
    with open(base_path / "instruction.json", "r") as file_pointer:
        instructions = json.load(file_pointer)
    crs = instructions["rivers"]["output"]["crs"]["horizontal"]

    ## Create results director
    results_dir = cache_path / instructions["dem"]["data_paths"]["subfolder"]
    results_dir.mkdir()

    ## Amend paths (cache and river files) in instruction file
    # cache_path
    instructions["rivers"]["data_paths"]["local_cache"] = str(cache_path)
    instructions["drains"]["data_paths"]["local_cache"] = str(cache_path)
    instructions["dem"]["data_paths"]["local_cache"] = str(cache_path)
    instructions["roughness"]["data_paths"]["local_cache"] = str(cache_path)
    # catchment_boundary path
    instructions["drains"]["data_paths"]["catchment_boundary"] = str(
        cache_path / instructions["dem"]["data_paths"]["catchment_boundary"]
    )
    instructions["dem"]["data_paths"]["catchment_boundary"] = str(
        cache_path / instructions["dem"]["data_paths"]["catchment_boundary"]
    )
    instructions["roughness"]["data_paths"]["catchment_boundary"] = str(
        cache_path / instructions["dem"]["data_paths"]["catchment_boundary"]
    )
    # river flow, friction and network files
    instructions["rivers"]["rivers"]["rec_file"] = str(
        cache_path / instructions["rivers"]["rivers"]["rec_file"]
    )
    instructions["rivers"]["rivers"]["flow_file"] = str(
        cache_path / instructions["rivers"]["rivers"]["flow_file"]
    )

    ## Save the amended instructions in cylc run cache
    with open(base_path / "instruction.json", "w") as file_pointer:
        json.dump(instructions, file_pointer, indent=4)

    ## Load in catchment
    catchment = geopandas.read_file(instructions["dem"]["data_paths"]["catchment_boundary"])
    # Explicitly override as CRS isn't being read in correctly.
    catchment.set_crs(crs, inplace=True, allow_override=True)

    ## Load in LiDAR files
    print("Download LiDAR files")
    lidar_fetcher = geoapis.lidar.OpenTopography(
        cache_path=cache_path, search_polygon=catchment, verbose=True
    )
    lidar_fetcher.run("Wellington_2013")
    print("Finished setup!")


if __name__ == "__main__":
    main()
