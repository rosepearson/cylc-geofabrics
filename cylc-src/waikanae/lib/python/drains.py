# -*- coding: utf-8 -*-
"""
Run the geofabrics.processor.DrainBathymetryGenerator pipeline
"""

import json
import pathlib
import dotenv
import os
#import geofabrics.processor

def main():
    """ The drains.main function updates sets the LINZ API keys, reads the
    instruction file in, and runs the geofabrics drains processing pipeline.
    This pipeline generates drain bathymetry information to be read into
    the geofabrics HydrologicDemGenerator pipeline.
    """

    print('Run the drains task!')

    # Setup the paths
    base_path = pathlib.Path().cwd().parent.parent.parent

    # Setup the LINZ API keys
    dotenv.load_dotenv(base_path / ".env")
    linz_key = os.environ.get("LINZ_API", None)

    # Read in the instruction file
    with open(base_path / "instruction.json", "r") as file_pointer:
        instructions = json.load(file_pointer)

    # Launch the geofabrics processing routine
    '''runner = geofabrics.processor.DrainBathymetryGenerator(
        cls.instructions["drains"], debug=False
    )'''


if __name__ == "__main__":
    main()