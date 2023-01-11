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

    ## Define cylc paths
    # note if calling python direct use: 'cylc_run_base_path = pathlib.Path().cwd()'
    #cylc_run_base_path = pathlib.Path().cwd().parent.parent.parent
    cylc_run_base_path = pathlib.Path().cwd().parent.parent
    cylc_run_cache_path = cylc_run_base_path / "geofabrics_cache"
    cylc_run_inputs_path = cylc_run_base_path / "catchments"
    catchment_id = "029"
    
    ## Create results directory
    subfolder = "results"
    cylc_run_results_dir = cylc_run_cache_path / subfolder
    cylc_run_results_dir.mkdir(parents=True, exist_ok=True)
    
    ## Define catchment boundary
    catchment_boundary_path = cylc_run_inputs_path / "catchments" / f"{catchment_id}_large.geojson"
    
    ## Read in the parameter files
    with open(cylc_run_inputs_path / "parameters" / "global.json", "r") as file_pointer:
        global_parameters = json.load(file_pointer)
    with open(cylc_run_inputs_path / "parameters" / f"{catchment_id}.json", "r") as file_pointer:
        catchment_parameters = json.load(file_pointer)
    
    ## Pull out global paths
    cache_path = pathlib.Path(global_parameters["shared"]["data_paths"].pop("global_cache"))
    network_path = cache_path / global_parameters["rivers"]["rivers"].pop("network_file_relative_path")
    
    ## Set global paths
    global_parameters["shared"]["data_paths"]["local_cache"] = str(cylc_run_cache_path)
    global_parameters["shared"]["data_paths"]["subfolder"] = subfolder
    global_parameters["rivers"]["rivers"]["network_file"] = network_path
    global_parameters["shared"]["data_paths"]["catchment_boundary"] = str(catchment_boundary_path)
    
    ## Add in the LINZ API key and add to the instruction file
    # Load the LINZ API keys
    dotenv.load_dotenv(cylc_run_base_path / ".env")
    linz_key = os.environ.get("LINZ_API", None)
    # Add the LINZ API key
    global_parameters["shared"]["apis"]["vector"]["linz"]["key"] = linz_key

    ## Create instruction file from the parameter files
    # Populate with the global shared values
    instructions = {"rivers": global_parameters["shared"],
                    "waterways": global_parameters["shared"],
                    "dem": global_parameters["shared"],
                    "roughness": global_parameters["shared"]}
    # Add the stage specific global values
    instructions["rivers"] = {**instructions["rivers"],**global_parameters["rivers"]}
    instructions["waterways"] = {**instructions["waterways"],**global_parameters["waterways"]}
    instructions["dem"] = {**instructions["dem"],**global_parameters["dem"]}
    instructions["roughness"] = {**instructions["roughness"],**global_parameters["roughness"]}
    # Add the stage specific catchment values
    instructions["rivers"] = {**instructions["rivers"],**catchment_parameters["rivers"]}
    instructions["waterways"] = {**instructions["waterways"],**catchment_parameters["waterways"]}
    instructions["dem"] = {**instructions["dem"],**catchment_parameters["dem"]}
    instructions["roughness"] = {**instructions["roughness"],**catchment_parameters["roughness"]}
    ## TODO - may need to set above at each level of the dictionary
    print(instructions)
    ## Rivers specific setup
    instructions["rivers"]["data_paths"]["land"] = f"river_catchment_{instructions['rivers']['rivers']['area_threshold']}.geojson"
    instructions["rivers"]["vector"]["linz"]["land"].pop()
    instructions["rivers"]["data_paths"]["catchment_boundary"].pop()
    
    ## Roughness - set final output to global cache
    output_geofabric_path = cache_path / catchment_id / "ancil" / "bgflood" / "geofabrics" ## TODO consider pulling out into global - or an unversioned usecase specific json
    output_geofabric_path.parents[0].mkdir(parents=True, exist_ok=True)
    instructions["roughness"]["data_paths"]["result_geofabric"] = output_geofabric_path / str(instructions["roughness"]["output"]["grid_params"]["resolution"]) + "_geofabric.nc"
    
    
    ## write out the JSON instruction file
    with open(cylc_run_base_path / "instruction.json", "w") as json_file:
        json.dump(instructions, json_file, indent=4)
    ## TODO - may want to scrub the LINZ key info
        
    ## Load in catchment
    crs = global_parameters["shared"]["output"]["crs"]["horizontal"]
    catchment = geopandas.read_file(catchment_boundary_path)
    catchment.set_crs(crs, inplace=True, allow_override=True) # TODO - Remove explicite override as CRS isn't being read in correctly.

    ## Load in LiDAR files
    print("Download LiDAR files")
    lidar_fetcher = geoapis.lidar.OpenTopography(cache_path=cylc_run_cache_path, search_polygon=catchment, verbose=True)
    lidar_fetcher.run(next(iter(catchment_parameters["apis"]["open_topography"]["lidar"])))
    print("Finished setup!")


if __name__ == "__main__":
    main()
