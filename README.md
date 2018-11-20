# Tip Detector

Provides a script to find the untraced tips of neuronal skeletons stored in DVID.  It uses libraries for analyzing
skeletons available in Neutu.

## Installation

Install [neutu](https://github.com/janelia-flyem/NeuTu) using conda.  To install this package,
set your conda environment to the neutu installation and then run setup:

	% python setup.py install

## Usage

To run the script call:

	% tipdetect "dvid server" "uuid" "segmentation name" "body id" "synapse name"

This will identify tips for the provided body id and load TODOs in DVID.  It will avoid
adding TODOs near PSDs as these should denote proper termination.  It currently dumps all the locations
to the terminal as well.

Note:

* The neuron must already have a skeleton computed.
* Requires write access to DVID.  The script could be easily modified to avoid writing to DVIDS and just dump the tip locations.
* The default distance to filter PSDs is 10 pixels.  This can be changed by copying 'loadtips.py' to a local directory and changing synfilter = 10 (set to 0 to turn off)
* TODOs are loaded as potential mergers, old todos are not deleted

