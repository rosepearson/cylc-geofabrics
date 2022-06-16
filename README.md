# Cylc-GeoFabrics
A repository to get Cylc setup running GeoFabrics over a catchment.

## NeSI setup
This is designed to run on the NeSI HPC. Basic [NeSI help](https://support.nesi.org.nz/hc/en-gb)

The following instructions are for getting the environment setup for a fresh run.

```
# Move to the project
cd /nesi/project/nesi/niwa03440/Cylc-GeoFabrics
cd cylc-src/graph-introduction # This should contain a cylc-flow file

# Load cylc
module purge
pip install cylc-flow --user

cylc graph .

```
