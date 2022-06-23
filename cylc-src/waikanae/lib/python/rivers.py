# -*- coding: utf-8 -*-
"""
Run rivers
"""
import json
import pathlib
import dotenv
#import geofabrics

def main():
    """ The rivers.main function updates sets the LINZ API keys, reads the
    instruction file in, and runs the geofabrics rivers processing pipeline.
    """

    print('Run rivers!')

    # Setup the paths
    base_path = pathlib.Path().cwd().parent.parent.parent

    # Setup the LINZ API keys
    dotenv.load_dotenv(base_path / ".env")
    linz_key = os.environ.get("LINZ_API", None)

    # Read in the instruction file
    with open(base_path / "instruction.json", "r") as file_pointer:
        instructions = json.load(file_pointer)

    # Launch the geofabrics processing routine
    '''runner = processor.RiverBathymetryGenerator(
        cls.instructions["rivers"], debug=False
    )'''


if __name__ == "__main__":
    main()