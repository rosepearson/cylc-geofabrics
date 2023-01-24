# -*- coding: utf-8 -*-
"""
Run setup - download needed LiDAR files
"""

import argparse
import json
import pathlib
import dotenv
import os
import geoapis
import geoapis.lidar
import geopandas
import copy


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


def merge_dicts(dict_a: dict, dict_b: dict, replace_a: bool):
    """ Merge the contents of the dict_a and dict_b. Use recursion to merge
    any nested dictionaries. replace_a determines if the dict_a values are
    replaced or not if different values are in the dict_b.
    
    Adapted from https://stackoverflow.com/questions/7204805/how-to-merge-dictionaries-of-dictionaries

    Parameters:
            base_dict  The dict to 
            new_dict  The location of the centre of the river mouth
            replace_a If True any dict_a values are replaced if different values are in dict_b
    """
    def recursive_merge_dicts(base_dict: dict, new_dict: dict, replace_base: bool, path: list = []):
        """ Recurively add the new_dict into the base_dict. dict_a is mutable."""
        for key in new_dict:
            if key in base_dict:
                if isinstance(base_dict[key], dict) and isinstance(new_dict[key], dict):
                    recursive_merge_dicts(base_dict=base_dict[key], new_dict=new_dict[key], 
                                          replace_base=replace_base, path=path + [str(key)])
                elif base_dict[key] == new_dict[key]:
                    pass # same leaf value
                else:
                    if replace_base:
                        print(f"Conflict with both dictionaries containing different values at {path + [str(key)]}."
                              " Value replaced.")
                        base_dict[key] = new_dict[key]
                    else:
                        print(f"Conflict with both dictionaries containing different values at {path + [str(key)]}"
                              ". Value ignored.")
            else:
                base_dict[key] = new_dict[key]
        return base_dict
    
    return recursive_merge_dicts(copy.deepcopy(dict_a), dict_b, replace_base=replace_a)


def main(catchment_id: str):
    """ The setup.setup_instructions function constructs the instruction file for the specified catchment. """

    print("Run setup!")

    ## Define cylc paths
    # note if calling python direct use: 'cylc_run_base_path = pathlib.Path().cwd().parent.parent'
    cylc_run_base_path = pathlib.Path().cwd().parent.parent.parent
    cylc_run_cache_path = cylc_run_base_path / "geofabrics_cache"
    cylc_run_inputs_path = cylc_run_base_path / "catchments"
    
    ## Create results directory
    cylc_run_results_dir = cylc_run_cache_path / catchment_id
    cylc_run_results_dir.mkdir(parents=True, exist_ok=True)
    
    ## Define catchment boundary
    catchment_boundary_path = cylc_run_inputs_path / "catchments" / f"{catchment_id}.geojson"
    
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
    global_parameters["shared"]["data_paths"]["subfolder"] = catchment_id
    global_parameters["shared"]["data_paths"]["catchment_boundary"] = str(catchment_boundary_path)
    global_parameters["rivers"]["rivers"]["network_file"] = str(network_path)
    
    ## Add in the LINZ API key and add to the instruction file
    # Load the LINZ API keys
    dotenv.load_dotenv(cylc_run_base_path / ".env")
    linz_key = os.environ.get("LINZ_API", None)
    # Add the LINZ API key
    global_parameters["shared"]["apis"]["vector"]["linz"]["key"] = linz_key

    ## Create instruction file from the parameter files
    # Populate with the global shared values
    shared = merge_dicts(dict_a=global_parameters["shared"], dict_b=catchment_parameters["shared"], replace_a=True)
    instructions = {"rivers": shared, "waterways": shared, "dem": shared, "roughness": shared}
    # Add the stage specific global values
    for key in instructions.keys():
        if key in global_parameters:
            instructions[key] = merge_dicts(instructions[key], global_parameters[key], replace_a=True)
    # Add the stage specific catchment values
    for key in instructions.keys():
        if key in catchment_parameters:
            instructions[key] = merge_dicts(instructions[key], catchment_parameters[key], replace_a=True)
    
    ## Rivers specific setup
    instructions["rivers"]["data_paths"]["land"] = f"river_catchment_{instructions['rivers']['rivers']['area_threshold']}.geojson"
    instructions["rivers"]["apis"]["vector"]["linz"].pop("land")
    instructions["rivers"]["data_paths"].pop("catchment_boundary")
    
    ## Roughness - set final output to global cache
    ## TODO consider pulling out into global - or an unversioned usecase specific json
    output_geofabric_path = cache_path / catchment_id / "ancil" / "bgflood" / "geofabrics" 
    output_geofabric_path.parents[0].mkdir(0o755, parents=True, exist_ok=True)
    instructions["roughness"]["data_paths"]["result_geofabric"] = str(output_geofabric_path / f"{instructions['roughness']['output']['grid_params']['resolution']}m_geofabric.nc")

    
    ## write out the JSON instruction file - TODO - may want to scrub the LINZ key info
    with open(cylc_run_cache_path / catchment_id / "instruction.json", "w") as json_file:
        json.dump(instructions, json_file, indent=4)
    
    print("Finished!")


if __name__ == "__main__":
    """ If called as script: Read in the args and launch the main function"""
    args = parse_args()
    main(catchment_id=args.catchment_id)
