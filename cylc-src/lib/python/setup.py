# -*- coding: utf-8 -*-
"""
Run setup - download needed LiDAR files
"""

import json
import pathlib
import dotenv
import os
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
    cylc_run_base_path = pathlib.Path().cwd().parent.parent.parent
    cylc_run_cache_path = cylc_run_base_path / "data"
    cache_path = pathlib.Path("/nesi/project/niwa03440/cylc_test/")
    rec_data_path = cache_path / "data/REC2/"

    ## Read in the instruction file
    with open(cylc_run_base_path / "instruction.json", "r") as file_pointer:
        instructions = json.load(file_pointer)
    crs = instructions["rivers"]["output"]["crs"]["horizontal"]

    ## Create results director
    subfolder = instructions["dem"]["data_paths"]["subfolder"]
    cylc_run_results_dir = cylc_run_cache_path / subfolder
    cylc_run_results_dir.mkdir(parents=False, exist_ok=False)

    ## Amend paths (cache and river files) in instruction file
    # cache_path
    instructions["rivers"]["data_paths"]["local_cache"] = str(cylc_run_cache_path)
    instructions["drains"]["data_paths"]["local_cache"] = str(cylc_run_cache_path)
    instructions["dem"]["data_paths"]["local_cache"] = str(cylc_run_cache_path)
    instructions["roughness"]["data_paths"]["local_cache"] = str(cylc_run_cache_path)
    # catchment_boundary path
    catchment_boundary = instructions["dem"]["data_paths"]["catchment_boundary"]
    instructions["drains"]["data_paths"]["catchment_boundary"] = str(
        cylc_run_cache_path / catchment_boundary
    )
    instructions["dem"]["data_paths"]["catchment_boundary"] = str(
        cylc_run_cache_path / catchment_boundary
    )
    instructions["roughness"]["data_paths"]["catchment_boundary"] = str(
        cylc_run_cache_path / catchment_boundary
    )
    # final geofabric output to overal cylc cache location
    output_geofabric_path = cache_path / instructions["roughness"]["data_paths"]["result_geofabric"]
    instructions["roughness"]["data_paths"]["result_geofabric"] = str(
        output_geofabric_path
    )
    output_geofabric_path.parents[0].mkdir(parents=True, exist_ok=True)
    
    # river flow, friction and network files
    instructions["rivers"]["rivers"]["rec_file"] = str(
        rec_data_path / instructions["rivers"]["rivers"]["rec_file"]
    )
    instructions["rivers"]["rivers"]["flow_file"] = str(
        rec_data_path / instructions["rivers"]["rivers"]["flow_file"]
    )

    ## Load in the LINZ API key and add to the instruction file
    # Load the LINZ API keys
    dotenv.load_dotenv(cylc_run_base_path / ".env")
    linz_key = os.environ.get("LINZ_API", None)
    # Add the LINZ API key
    instructions["rivers"]["apis"]["linz"]["key"] = linz_key
    instructions["drains"]["apis"]["linz"]["key"] = linz_key
    instructions["dem"]["apis"]["linz"]["key"] = linz_key
    instructions["roughness"]["apis"]["linz"]["key"] = linz_key

    ## Save the amended instructions in cylc run cache
    with open(cylc_run_base_path / "instruction.json", "w") as file_pointer:
        json.dump(instructions, file_pointer, indent=4)

    ## Load in catchment
    catchment = geopandas.read_file(instructions["dem"]["data_paths"]["catchment_boundary"])
    # Explicitly override as CRS isn't being read in correctly.
    catchment.set_crs(crs, inplace=True, allow_override=True)

    ## Load in LiDAR files
    print("Download LiDAR files")
    lidar_fetcher = geoapis.lidar.OpenTopography(
        cache_path=cylc_run_cache_path, search_polygon=catchment, verbose=True
    )
    lidar_fetcher.run("Wellington_2013")
    print("Finished setup!")


if __name__ == "__main__":
    main()
