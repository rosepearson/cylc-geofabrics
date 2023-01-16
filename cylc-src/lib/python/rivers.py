# -*- coding: utf-8 -*-
"""
Run the geofabrics.processor.RiverBathymetryGenerator pipeline
"""

import json
import pathlib
import geofabrics.processor


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


def main(catchment_id: str):
    """ The rivers.main function reads the instruction file in, and
    runs the geofabrics.processor.RiverBathymetryGenerator pipeline.
    This pipeline generates drain bathymetry information to be read into
    the geofabrics HydrologicDemGenerator pipeline.
    """

    print('Run the rivers task!')

    # Setup the paths
    base_path = pathlib.Path().cwd().parent.parent.parent
    catchment_path = base_path / "geofabrics_cache" / catchment_id

    # Read in the instruction file
    with open(catchment_path / "instruction.json", "r") as file_pointer:
        instructions = json.load(file_pointer)

    # Launch the geofabrics processing routine
    runner = geofabrics.processor.RiverBathymetryGenerator(
        instructions["rivers"], debug=False
    )
    runner.run()
    print("Finished!")


if __name__ == "__main__":
    """ If called as script: Read in the args and launch the main function"""
    args = parse_args()
    setup_instructions(catchment_id=args.catchment_id)
