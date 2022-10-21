# Cylc-GeoFabrics
A repository for using Cylc 8 to run GeoFabrics over a catchment.

Table of contents:
* Current status
* Session setup
* Initial Cylc and NeSI setup (read through if you haven't used this before!)

# Current status
*__This is setup and ready and has been run over Waikanae. The results for Waiakane are written in /nesi/project/niwa03440/cylc_test/029/geofabrics/hydrological_geofabric.nc__*

# Session setup
The following instructions are for getting Cylc 8 setup for a fresh session. Open a fresh bash terminal and run the following.

```
# Setup paths to access Cylc
module purge
module load NeSI
module load Miniconda3
export PATH=/opt/nesi/share/cylc/etc/bin:$PATH
export CYLC_VERSION=8.0rc3
export PROJECT=niwa03440
```

# Waikanae
If you want to try things out without running over the full Waikanae catchment, you can change the instruction.json file to read in the "small.json" instead of the "large.geojson" catchment_boundary file.

## Running
The following is a shell example for running the cylc workflow for creating a geofabric for Waikanae. 

```
# Move to the waikanae example
cd /nesi/project/niwa03440/cylc-geofabrics/cylc-src/waikanae

# Install, run and monitor the cylc workflow
cylc validate . # Check for errors and correct as needed
cylc install
cylc play waikanae
cylc tui waikanae

# View outputs while `cylc cat-log -f o waikanae//runN/setup` is fixed
cylc cat-log -f e waikanae//1/setup # Error output
cylc cat-log -f o waikanae//1/setup # Output
cat /home/pearsonra/cylc-run/waikanae/runN/log/job/1/setup/NN/job.out

# Clean runs
cylc clean waikanae

```

## Scheduler info
The following will generate a png of the Waikanae Cylc workflow

```
# Move to the project and basic scheduling example
cd /nesi/project/niwa03440/cylc-geofabrics/cylc-src/waikanae


# Create a cylc graph from the cylc.flow file
cylc graph . -o graph.png

```

# Initial Cylc and NeSI setup
This Cylc 8 suite is designed to be run on the NeSI  Maui HPC ([NeSI help](https://support.nesi.org.nz/hc/en-gb)). There are various configuration steps that may need to be performed before your first run, which are mainly explained in [Cylc 8 on Maui - One NIWA](https://one.niwa.co.nz/pages/viewpage.action?spaceKey=HPCF&title=Cylc+8+on+Maui). This also includes some worked examples.

Two key sections are expaned on below:
* SSH setup - see section below
* Cylc global.config - see section below 

## SSH setup
You will need an ssh key without a password and add it to your authorized_keys file to allow ssh forwarding without a password being entred.

To do this run the following and press entre when prompted to entre a password. 

```
ssh-keygen
cat ~/.ssh/id_ssh_rsa.pub >> ~/.ssh/authorized_keys`
```

Note you will need all folders only to have read access and you will need to set the authorized_keys to be read only as well. See [Cylc 8 on Maui - One NIWA](https://one.niwa.co.nz/pages/viewpage.action?spaceKey=HPCF&title=Cylc+8+on+Maui) for more details.

Once you have configued your SSH key, make sure to check you have access to the w-cylc01, w-cylc02, and w-cylc03 nodes. If you don't have access request permission as described in [Cylc 8 on Maui - One NIWA](https://one.niwa.co.nz/pages/viewpage.action?spaceKey=HPCF&title=Cylc+8+on+Maui).

## Cylc global.cylc setup
If you are running Cylc on an interative session on Mahuika accessed via the JupyterHub portal, you will need to explicitly ensure the w-cylc01 .. 03 nodes are avaliable. This can be done by adding the following to a global.cylc file located in `~/.cylc/flow/8.0rc3/global.cylc`. 

```
	[scheduler]
	    [[run hosts]]
	        available = w-cylc01, w-cylc02, w-cylc03
```

You may also need to explicitly add a mahuika platform if it does not show up as one of the listed platforms when you run `cylc config`. This is particularly nessecary if you NIWA/NeSI project only has permission to run on Mahuika and not Maui. This can be done by adding the following to a global.cylc file located in `~/.cylc/flow/8.0rc3/global.cylc`. 

```
[platforms]
   [[mahuika-slurm]]
        hosts = mahuika01.mahuika.nesi.org.nz, mahuika02.mahuika.nesi.org.nz
        install target = localhost
        job runner = slurm
```
This platform can then be specified in any of the cylc runtime tasks.

## Conda environment setup 
Currently the flow relies on an a conda environment being created before running cylc. In future this may be done as part of the setup stage. See this [link](https://gist.github.com/matthewrmshin/74a7b78adecd297b40e64f6c867b316b) for an example.

Execute the following in the bash terminal. Check there are no errors. Note that the environment is created in a shared location so it may be accessed by others working on the niwa03440 project.

```
# Setup conda environment
cd /nesi/project/niwa03440/cylc-geofabrics/cylc-src
conda env create -f environment.yml -p /nesi/project/niwa03440/conda/envs/geofabrics

```

A note on removing environments if they need to be recreated: `conda remove --name geofabrics --all`

## LINZ API key
The LINZ Data Service (LDS) requires an API key. This is stored in a `.env` file in `cylc-geofabrics/cylc-src/waikanae/.env` on NeSI, but it is not versioned as that would be a security risk. Refer to [this page](https://github.com/rosepearson/GeoFabrics/wiki/Testing-and-GitHub-Actions) if you need to generate a new `.env` file.


# Todo
* [ ] Work through getting geoapis and geofabrics published on Conda-Forge. See [PR](https://github.com/conda-forge/staged-recipes/pull/19342)
* [ ] Update the setup.py to create a full instructions.json from a minimal list of parameters
* [ ] Introduce environment variables / arguments to parameterise the flow.cylc and python scripts (i.e. to set the location to write out to, and the catchment to process)
* [ ] Restructure the suite to allow it to be applied to any catchment

# Running GeoFabrics directly on the HPC
The following section gives instructions for running GeoFabrics directly on the HPC. 

## Instructions for a generic new HPC
1. The recommended file structures is:
```
 - geofabrics
   |- GeoFabrics (the repo - https://github.com/rosepearson/GeoFabrics)
   |- caches (folder the caches will end up in)
   |- catchments (folder containing the geometry files (i.e geojson) refenced in the instruction files)
   |- instructions (folder containing the instruction files used to run GeoFabrics)
```
2. Get a local copy of the GeoFabrics [repo](https://github.com/rosepearson/GeoFabrics)
3. Create or copy catchment and instruction files to get started
   * See https://github.com/rosepearson/GeoFabrics/tree/main/tests for example instruction files
   * See [/nesi/project/niwa03440/geofabrics](/nesi/project/niwa03440/geofabrics) for an example with full-size instruction files and catchments
4. See _4. Run an instruction_ in the following section for an example of how to run GeoFabrics

## Instructions specific to NeSI & niwa03440
1. Navigate to [/nesi/project/niwa03440/geofabrics](/nesi/project/niwa03440/geofabrics)
2. Check [/nesi/project/niwa03440/geofabrics/GeoFabrics](/nesi/project/niwa03440/geofabrics) is on the branch you are trying to test
4. Run an instruction
    i. Directly in Python
        * `cd /nesi/project/niwa03440/geofabrics/GeoFabrics/src`
        * Directly in Python: `python -m main --instruction /nesi/project/niwa03440/geofabrics/instructions/instruction_dem_only.json`
    ii. Using Slurm
        * `cd /nesi/project/niwa03440/geofabrics`
        * `sbatch westport.sl`

