# -*- coding: utf-8 -*-
"""
Run the geofabrics.processor.RoughnessLengthGenerator pipeline
"""

import json
import pathlib
import geofabrics.processor

def main():
    """ The roughness.main function reads the instruction file in, and
    runs the geofabrics.processor.RoughnessLengthGenerator pipeline.
    This pipeline combines different source information into a
    hydrologically conditioned DEM.
    """

    print('Run the roughness task!')

    # Setup the paths
    base_path = pathlib.Path().cwd().parent.parent.parent

    # Read in the instruction file
    with open(base_path / "instruction.json", "r") as file_pointer:
        instructions = json.load(file_pointer)

    # Launch the geofabrics processing routine
    runner = geofabrics.processor.RoughnessLengthGenerator(
        instructions["roughness"]
    )
    runner.run()


if __name__ == "__main__":
    main()