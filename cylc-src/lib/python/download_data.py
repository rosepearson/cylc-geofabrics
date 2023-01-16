# -*- coding: utf-8 -*-
"""
Run setup - download needed LiDAR files
"""

import json
import pathlib
import geoapis
import geoapis.lidar
import geoapis.vector
import geopandas


def download_vector_layer(vector_instructions: dict, 
                          key: str, 
                          local_cache: str, 
                          catchment: geopandas.GeoDataFrame):
    print(f"Downloading vector layer: {key}")
    fetcher = geoapis.vector.Linz(vector_instructions["key"], 
                                        bounding_polygon=catchment, verbose=True)
    for layer in vector_instructions[key]["layers"]:
        # Use the run method to download each layer in turn
        vector = fetcher.run(layer)

        # Ensure directory for layer and save vector file
        layer_dir = pathlib.Path(local_cache) / "vector"
        layer_dir.mkdir(parents=True, exist_ok=True)
        vector.to_file(layer_dir / f"{layer}.geojson")

def main():
    """ The download_lidar.main function downloads all LiDAR data required for the later
    GeoFabrics processing steps. """

    print("Run setup!")

    ## Define cylc paths
    # note if calling python direct use: 'cylc_run_base_path = pathlib.Path().cwd().parent.parent'
    cylc_run_base_path = pathlib.Path().cwd().parent.parent.parent
    
    ## Read in the instruction file
    with open(cylc_run_base_path / "instruction.json", "r") as file_pointer:
        instructions = json.load(file_pointer)
     
    ## Load in catchment
    catchment = geopandas.read_file(instructions["dem"]["data_paths"]["catchment_boundary"])

    ## Load in LiDAR files
    print("Download LiDAR files")
    lidar_fetcher = geoapis.lidar.OpenTopography(cache_path=instructions["dem"]["data_paths"]["local_cache"], 
                                                 search_polygon=catchment, verbose=True)
    lidar_fetcher.run(next(iter(instructions["dem"]["apis"]["lidar"]["open_topography"])))
    
    print("Download vector files")
    linz_vector_instruction = instructions["dem"]["apis"]["vector"]["linz"]
    download_vector_layer(vector_instructions=linz_vector_instruction, key="land", 
                          local_cache=instructions["dem"]["data_paths"]["local_cache"],
                         catchment=catchment)
    download_vector_layer(vector_instructions=linz_vector_instruction, key="bathymetry_contours",
                          local_cache=instructions["dem"]["data_paths"]["local_cache"],
                         catchment=catchment)
    print("Finished!")
    

if __name__ == "__main__":
    """If called as a script."""
    main()
