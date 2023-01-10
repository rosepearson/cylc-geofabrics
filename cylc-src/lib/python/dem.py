# -*- coding: utf-8 -*-
"""
Run the geofabrics.processor.HydrologicDemGenerator pipeline
"""

import json
import pathlib
import geofabrics.processor

def main():
    """ The dem.main function reads the instruction file in, and
    runs the geofabrics.processor.HydrologicDemGenerator pipeline.
    This pipeline combines different source information into a
    hydrologically conditioned DEM.
    """

    print('Run the dem task!')

    # Setup the paths
    base_path = pathlib.Path().cwd().parent.parent.parent

    # Read in the instruction file
    with open(base_path / "instruction.json", "r") as file_pointer:
        instructions = json.load(file_pointer)

    # Launch the geofabrics processing routine
    runner = geofabrics.processor.HydrologicDemGenerator(
        instructions["dem"]
    )
    runner.run()


if __name__ == "__main__":
    main()