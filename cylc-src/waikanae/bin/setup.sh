#!/bin/bash
#------------------------------------------------------------------------------
# This script is used to activate a preexisting conda environment
# ------------------------------------------------------------------------------
# Note: "conda" does not work with "set -u"

set +u # allow unbound variables
conda activate geofabrics # or whatever
set -u # disallow them again, before carrying on