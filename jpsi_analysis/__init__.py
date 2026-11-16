"""J/psi to mu mu, 2023

Study of prompt J/psi -> mu+ mu- in Run3Summer23 simulation (2023, no pileup).
"""

import os

# Absolute path of this package: configs/, data/ and friends are found relative to it,
# so the analysis runs the same from a notebook, a script or a batch worker.
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# Name of the TTree that holds the events in the input files.
TREE_NAME = "Events"

# Run period of a sample whose config names none ("" for none). The periods are in
# configs/run_periods.yaml.
YEAR = "2023"

__version__ = "0.1.0"
