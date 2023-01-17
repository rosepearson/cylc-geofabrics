# -*- coding: utf-8 -*-
"""
Run setup - download needed LiDAR files
"""

import json
import pathlib
import geoapis
import dotenv
import os
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
    """ The download all LiDAR and most vector data required for the later
    GeoFabrics processing steps. """

    print("Run setup!")

    ## Define cylc paths
    # note if calling python direct use: 'cylc_run_base_path = pathlib.Path().cwd().parent.parent'
    base_path = pathlib.Path().cwd().parent.parent.parent
    cache_path = base_path / "geofabrics_cache"
    
    ## Read in the global parameters file
    print("Read in the global parameter file")
    with open(base_path / "catchments" / "parameters" / "global.json", "r") as file_pointer:
        instructions = json.load(file_pointer)
        
    ## Get LINZ key
    dotenv.load_dotenv(base_path / ".env")
    linz_key = os.environ.get("LINZ_API", None)

    
    print("Download shared vector data")
    linz_vector_instruction = instructions["shared"]["apis"]["vector"]["linz"]
    linz_vector_instruction["key"] = linz_key
    for key in linz_vector_instruction:
        if key != "key":
            download_vector_layer(vector_instructions=linz_vector_instruction, 
                                  key=key, 
                                  local_cache=cache_path,
                                  catchment=None)
    print("Finished!")
    

if __name__ == "__main__":
    """ If called as script: Read in the args and launch the main function"""
    main()
