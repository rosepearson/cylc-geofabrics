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
    print(pathlib.Path().cwd())
    
    # define paths
    base_path = pathlib.Path().cwd().parent.parent.parent
    data_path = base_path / "data"
    
    # read in the instruction file
    with open(base_path / "instruction.json", "r") as file_pointer:
        instructions = json.load(file_pointer)
    crs = instructions["rivers"]["output"]["crs"]["horizontal"]
    
    # amend and save back out
    
    # load in catchment
    catchment = geopandas.read_file(data_path / "small.geojson")
    catchment.set_crs(crs, inplace=True, allow_override=True) # Note tempoarary while env setup correctly. CRS not being read in correctly
    print(catchment.crs)
    print(catchment.bounds)
    print(instructions["dem"]["data_paths"]["catchment_boundary"])
    
    # load in LiDAR files
    lidar_fetcher = geoapis.lidar.OpenTopography(cache_path=data_path, 
                                                 search_polygon=catchment, verbose=True)
    lidar_fetcher.run("Wellington_2013")
    
    


if __name__ == "__main__":
    main()