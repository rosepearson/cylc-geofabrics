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



def parse_args():
    """Expect a command line argument of the form:
    '--catchment_id id_string'"""

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--catchment_id",
        metavar="str",
        required=True,
        action="store",
        help="the catchment id string - The ID of the catchment to run over. Will use the json file of that name.",
    )

    return parser.parse_args()


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


def main(catchment_id: str):
    """ The download all LiDAR and most vector data required for the later
    GeoFabrics processing steps. """

    print("Run setup!")

    ## Define cylc paths
    # note if calling python direct use: 'cylc_run_base_path = pathlib.Path().cwd().parent.parent'
    base_path = pathlib.Path().cwd().parent.parent.parent
    
    ## Read in the instruction file
    with open(base_path / "catchments" / "parameters" / f"{catchment_id}.json", "r") as file_pointer:
        instructions = json.load(file_pointer)
     
    ## Load in catchment
    catchment = geopandas.read_file(base_path / "catchments" / "catchments" / f"{catchment_id}.geojson")

    ## Load in LiDAR files
    print("Download LiDAR files")
    lidar_fetcher = geoapis.lidar.OpenTopography(cache_path=instructions["shared"]["data_paths"]["local_cache"], 
                                                 search_polygon=catchment, verbose=True)
    lidar_fetcher.run(next(iter(instructions["dem"]["apis"]["lidar"]["open_topography"])))
    
    if "vector" in instructions["shared"]["apis"] or "linz" in instructions["shared"]["apis"]["vector"]:
        print("Download vector files")
        linz_vector_instruction = instructions["shared"]["apis"]["vector"]["linz"]
        for key in linz_vector_instruction:
            if key != "key":
                download_vector_layer(vector_instructions=linz_vector_instruction, 
                                      key=key, 
                                      local_cache=instructions["dem"]["data_paths"]["local_cache"],
                                      catchment=catchment)
    print("Finished!")
    

if __name__ == "__main__":
    """ If called as script: Read in the args and launch the main function"""
    args = parse_args()
    main(catchment_id=args.catchment_id)
