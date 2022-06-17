# Cylc-GeoFabrics
A repository to get Cylc setup running GeoFabrics over a catchment.

## NeSI setup
This is designed to run on the NeSI HPC. Basic [NeSI help](https://support.nesi.org.nz/hc/en-gb)

The following instructions are for getting the environment setup for a fresh run. Open a fresh bash terminal.

```
# Move to the project
cd /nesi/project/niwa03440/Cylc-GeoFabrics
cd cylc-src/graph-introduction # This should contain a cylc-flow file

# Setup paths to access Cylc
module purge
export PATH=/opt/nesi/share/cylc/etc/bin:$PATH
export CYLC_VERSION=8.0rc3

# Load cylc
module purge
module load Miniconda3/4.12.0
conda install -c conda-forge cylc-flow

# Create a cylc graph from the cylc-flow file
cylc graph .

```
