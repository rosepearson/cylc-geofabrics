# -*- coding: utf-8 -*-
"""
Run setup - Extract the catchment boundary for the specified catchment id
"""

import argparse


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

def setup_catchment(catchment_id: str):
    """ The setup.setup_catchment function extracts and saves the 
    catchment polygon as a geojson with the catchment_id as its name. """

    print(f"Run setup catchment for catchment {catchment_id}!")

    print("Currently does nothing in future will save bbox's of each catchment defined by https://git.niwa.co.nz/flood-resilience-aotearoa/create-flood-domains")
    print("Finished setup!")


def main():
    """ Read in the args and launch the setup function"""
    args = parse_args()
    setup_catchment(catchment_id=args.catchment_id)
    

if __name__ == "__main__":
    """If called as a script."""
    main()
