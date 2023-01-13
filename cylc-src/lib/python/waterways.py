# -*- coding: utf-8 -*-
"""
Run the geofabrics.processor.DrainBathymetryGenerator pipeline
"""

import json
import pathlib
import geofabrics.processor

def main():
    """ The drains.main function reads the instruction file in, and
    runs the geofabrics.processor.DrainBathymetryGenerator pipeline.
    This pipeline generates drain bathymetry information to be read into
    the geofabrics HydrologicDemGenerator pipeline.
    """

    print('Run the drains task!')

    # Setup the paths
    base_path = pathlib.Path().cwd().parent.parent.parent

    # Read in the instruction file
    with open(base_path / "instruction.json", "r") as file_pointer:
        instructions = json.load(file_pointer)

    # Launch the geofabrics processing routine
    runner = geofabrics.processor.WaterwayBedElevationEstimator(
        instructions["drains"], debug=False
    )
    runner.run()


if __name__ == "__main__":
    main()