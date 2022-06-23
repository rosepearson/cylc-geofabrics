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
    """ The setup.main function updates the paths in the instruction file based on the run location,
    and downloads all LiDAR data required for the later GeoFabrics processing steps. """
    print('Run setup!')
    
    # define paths - Note if testing with a direct python run use 'base_path = pathlib.Path().cwd()'
    base_path = pathlib.Path().cwd().parent.parent.parent
    data_path = base_path / "data"
    
    # read in the instruction file
    with open(base_path / "instruction.json", "r") as file_pointer:
        instructions = json.load(file_pointer)
    crs = instructions["rivers"]["output"]["crs"]["horizontal"]
    
    # amend paths (cache and river files) in instruction file and save back out
    instructions["rivers"]["data_paths"]["cache_path"] = str(data_path)
    instructions["rivers"]["rivers"]["rec_file"] = str(data_path / instructions["rivers"]["rivers"]["rec_file"])
    instructions["rivers"]["rivers"]["flow_file"] = str(data_path / instructions["rivers"]["rivers"]["flow_file"])
    instructions["drains"]["data_paths"]["cache_path"] = str(data_path)
    instructions["dem"]["data_paths"]["cache_path"] = str(data_path)
    instructions["roughness"]["data_paths"]["cache_path"] = str(data_path)
    with open(base_path / 'instruction.json', 'w') as file_pointer: # Override in cylc run cache
        json.dump(instructions, file_pointer, indent=4)
    
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