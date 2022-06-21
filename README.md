# Cylc-GeoFabrics
A repository to get Cylc setup running GeoFabrics over a catchment.

# Current status
*__The conda environment is mainly setup for geoapis, but I still need to work through including geofabrics. The cylc workflow skeleton exists. The setup tasks is finished and mostly working (runs locally fine, need to invetigate an environment related error that stops it progressing to the next steps). The remaining tasks need to be written - but will largely be a copy of the setup task and existing geofabrics tests__*

# NeSI setup
This is designed to run on the NeSI HPC. Basic [NeSI help](https://support.nesi.org.nz/hc/en-gb)

## Helpful links
Currently Cylc 8 only works on Maui. For detailed instructions and worked examples for using Cylc 8 on Maui see [Cylc 8 on Maui - One NIWA](https://one.niwa.co.nz/pages/viewpage.action?spaceKey=HPCF&title=Cylc+8+on+Maui)

## First time setup
You will need an ssh key without a password and add it to your authorized_keys file to allow ssh forwarding without a password being entred.

To do this run the following and press entre when prompted to entre a password. Note you will need all folders only to have read access and you will need to set the authorized_keys to be read only as well. Ask Hilary if you run into problems.

```
ssh-keygen
cat ~/.ssh/id_ssh_rsa.pub >> ~/.ssh/authorized_keys`
```

# Session setup
The following instructions are for getting Cylc 8 setup for a fresh session. Open a fresh bash terminal and run the following.

```
# Setup paths to access Cylc
module purge
module load Anaconda3
export PATH=/opt/nesi/share/cylc/etc/bin:$PATH
export CYLC_VERSION=8.0rc3
export PROJECT=niwa03440
```

## Conda environment setup
Currently this relies on an a conda environment being created before running cylc. In future this may be done as part of the setup stage. See this [link](https://gist.github.com/matthewrmshin/74a7b78adecd297b40e64f6c867b316b) for an example.

Execute the following in the bash terminal. Check there are no errors.

```
# Setup conda environment
cd /nesi/project/niwa03440/Cylc-GeoFabrics
conda env create -f environment.yml

```

A note on removing environments if they need to be recreated: `conda remove --name env_name --all`

## Running Waikanae
The following is a shell example for running the cylc workflow for creating a geofabric for Waikanae. It is still a work in progress. I currently downloads the required LiDAR files before exiting the setup stage with an error relating to the environment setup.

```
# Move to the waikanae example
cd /nesi/project/niwa03440/Cylc-GeoFabrics/cylc-src/waikanae

# Create a cylc graph from the cylc.flow file
cylc graph . -o graph.png

# Install and run the cylc file
cylc validate . # Check for errors and correct as needed
cylc install
cylc play waikanae

# View outputs while `cylc cat-log -f o waikanae//runN/setup` is fixed
cat /home/pearsonra/cylc-run/waikanae/runN/log/job/1/setup/NN/job.out

# Clean runs
cylc clean waikanae

```

## Basic Scheduling
The following is an example for a very basic scheduler

```
# Move to the project and basic scheduling example
cd /nesi/project/niwa03440/Cylc-GeoFabrics
cd cylc-src/graph-introduction # This should contain a cylc-flow file


# Create a cylc graph from the cylc.flow file
cylc graph . -o graph.png

```

# Todo
* [ ] Create a conda environment file for creating an environment for running geofabrics
  * [X] Create an environment for running geoapis
  * [ ] Extend the geoapis environment for also running geofabrics
* [X] Update the flow.cylc to activate the geoapis/geofabrics conda environment
* [ ] Update the python scripts for each task to call through to the relevant geofabrics functionality

## Later / Already done
* [ ] Waiting on geopais and geofabrics to be added to conda-forge so that they can be installed easily as part of a conda package. See [PR](https://github.com/conda-forge/staged-recipes/pull/19342)
  * The alternative is to create a Conda environment with a yml file with install from a git repository for both geoapis and geofabrics before running cylc
* [x] Add instructions for creating the conda environment. __Still to test__
* [x] Upload a test and full sized catchment file
* [x] Add a .env file containing the API keys for downloading vector data from LINZ to NeSI. This should not be put under version control
* [ ] Populate the python scripts controlling each of the cylc tasks.
