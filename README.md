# Cylc-GeoFabrics
A repository to get Cylc setup running GeoFabrics over a catchment.

# NeSI setup
This is designed to run on the NeSI HPC. Basic [NeSI help](https://support.nesi.org.nz/hc/en-gb)

## Helpful links
Currently Cylc 8 only works on Maui. For detailed instructions and worked examples for using Cylc 8 on Maui see [Cylc 8 on Maui - One NIWA](https://one.niwa.co.nz/pages/viewpage.action?spaceKey=HPCF&title=Cylc+8+on+Maui)

## First time setup
You will need an ssh key without a password and add it to your authorized_keys file to allow ssh forwarding without a password being entred. 

To do this run the following and press entre when prompted to entre a password. Ask Hilary if you run into problems.

```
ssh-keygen
cat ~/.ssh/id_ssh_rsa.pub >> ~/.ssh/authorized_keys`
```


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

# Waikanae-simple
The following is a shell example for creating a geofabric for Waikanae. At this stage it just prints "running xx" for each stage.

```
# Move to the waikanae example
cd /nesi/project/niwa03440/Cylc-GeoFabrics/cylc-src/waikanae

# Create a cylc graph from the cylc.flow file
cylc graph . -o graph.png

# Install and run the cylc file
cylc validate . # Check for errors and correct as needed
cylc install
cylc play waikanae 

```

# Todo
[ ] Waiting on geopais and geofabrics to be added to conda-forge so that they can be installed easily as part of a conda package. See [PR](https://github.com/conda-forge/staged-recipes/pull/19342)
  * The alternative is to create a Conda environment with a yml file with install from a git repository for both geoapis and geofabrics before running cylc
[ ] Add instructions for creating the conda environment
[ ] Upload a test and full sized catchment file
[x] Add a .env file containing the API keys for downloading vector data from LINZ to NeSI. This should not be put under version control
[ ] Populate the python scripts controlling each of the cylc tasks. 
