# Tip Detector

Provides a script to find the untraced tips of neuronal skeletons stored in DVID.  It uses libraries for analyzing
skeletons defined within [NeuTu](https://github.com/janelia-flyem/NeuTu).

## Installation

First install [miniconda](https://conda.io/miniconda.html).  Then do the following:

	% conda config --add channels conda-forge
	% conda config --add channels flyem-forge
	% conda create neutube-python -n neutube
	% source activate neutube
	% python setup.py install

## Usage

To run the script call:

	% tipdetect "dvid server" "uuid" "segmentation name" "body id" "synapse name"

This will identify tips for the provided body id and load TODOs in DVID.  It will avoid
adding TODOs near PSDs as these should denote proper process termination.  It currently dumps all the locations
to the terminal as well.

Note:

* The neuron must already have a skeleton computed.
* Requires write access to DVID.  The script could be easily modified to avoid writing to DVID and just dump the tip locations.
* The default distance to filter PSDs is 10 pixels.  This can be changed by changing synfilter = 10 (set to 0 to turn off)
* TODOs are loaded as potential mergers, old todos are not deleted

