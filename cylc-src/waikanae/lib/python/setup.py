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
    print('Run setup!')
    
    # define paths
    base_path = pathlib.Path().cwd().parent.parent.parent # pathlib.Path().cwd() # Uncomment for running directly (not through cylc)
    data_path = base_path / "data"
    
    # read in the instruction file
    with open(base_path / "instruction.json", "r") as file_pointer:
        instructions = json.load(file_pointer)
    crs = instructions["rivers"]["output"]["crs"]["horizontal"]
    
    # amend cache path, and rivers paths and save back out
    
    # load in catchment
    catchment = geopandas.read_file(data_path / "small.geojson")
    catchment.set_crs(crs, inplace=True, allow_override=True) # Explicitly override as CRS isn't being read in correctly.
    
    # load in LiDAR files
    print('Download LiDAR files')
    lidar_fetcher = geoapis.lidar.OpenTopography(cache_path=data_path, 
                                                 search_polygon=catchment, verbose=True)
    lidar_fetcher.run("Wellington_2013")
    print('Finished setup!')
    
    


if __name__ == "__main__":
    main()