# Cylc-GeoFabrics
A repository to get Cylc setup running GeoFabrics over a catchment.

# NeSI setup
This is designed to run on the NeSI HPC. Basic [NeSI help](https://support.nesi.org.nz/hc/en-gb)

## Helpful links
Currently Cylc 8 only works on Maui. For detailed instructions and worked examples for using Cylc 8 on Maui see [Cylc 8 on Maui - One NIWA](https://one.niwa.co.nz/pages/viewpage.action?spaceKey=HPCF&title=Cylc+8+on+Maui)

## Getting setup
The following instructions are for getting Cylc 8 setup for a fresh session. Open a fresh bash terminal.

```
# Setup paths to access Cylc
module purge
module load Anaconda3
export PATH=/opt/nesi/share/cylc/etc/bin:$PATH
export CYLC_VERSION=8.0rc3
export PROJECT=niwa03440
```

# Basic Scheduling
The following is an example for a very basic scheduler

```
# Move to the project and basic scheduling example
cd /nesi/project/niwa03440/Cylc-GeoFabrics
cd cylc-src/graph-introduction # This should contain a cylc-flow file


# Create a cylc graph from the cylc.flow file
cylc graph . -o graph.png

```

# Waikanae
The following is an example for creating a geofabric for Waikanae

```
# Move to the waikanae example
cd /nesi/project/niwa03440/Cylc-GeoFabrics/cylc-src/waikanae

# Create a cylc graph from the cylc.flow file
cylc graph . -o graph.png

# Install and run the cylc file
cylc validate # Check for errors and correct as needed
cylc install
cylc play waikanae


```
