# -*- coding: utf-8 -*-
"""
Run the geofabrics.processor.RawLidarDemGenerator pipeline
"""

import json
import pathlib
import geofabrics.processor

def main():
    """ The lidar.main function reads the instruction file in, and
    runs the geofabrics.processor.RawLidarDemGenerator pipeline.
    This pipeline generates a raw LiDAR DEM to be read into the geofabrics
    HydrologicDemGenerator pipeline.
    """

    print('Run the lidar task!')

    # Setup the paths
    base_path = pathlib.Path().cwd().parent.parent.parent

    # Read in the instruction file
    with open(base_path / "instruction.json", "r") as file_pointer:
        instructions = json.load(file_pointer)

    # Launch the geofabrics processing routine
    runner = geofabrics.processor.RawLidarDemGenerator(
        instructions["dem"])
    runner.run()


if __name__ == "__main__":
    main()