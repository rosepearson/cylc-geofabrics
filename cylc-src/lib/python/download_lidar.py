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
    """ The download_lidar.main function downloads all LiDAR data required for the later
    GeoFabrics processing steps. """

    print("Run setup!")

    ## Define cylc paths
    # note if calling python direct use: 'cylc_run_base_path = pathlib.Path().cwd().parent.parent'
    cylc_run_base_path = pathlib.Path().cwd().parent.parent.parent
    cylc_run_base_path = pathlib.Path().cwd().parent.parent
    
    ## Read in the instruction file
    with open(cylc_run_base_path / "instruction.json", "r") as file_pointer:
        instructions = json.load(file_pointer)
     
    ## Load in catchment
    catchment = geopandas.read_file(instructions["dem"]["data_paths"]["catchment_boundary"])

    ## Load in LiDAR files
    print("Download LiDAR files")
    lidar_fetcher = geoapis.lidar.OpenTopography(cache_path=instructions["dem"]["data_paths"]["local_cache"], search_polygon=catchment, verbose=True)
    lidar_fetcher.run(next(iter(instructions["dem"]["apis"]["lidar"]["open_topography"])))
    print("Finished setup!")
    

if __name__ == "__main__":
    """If called as a script."""
    main()
