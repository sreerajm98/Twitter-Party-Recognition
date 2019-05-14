"""
Python module for Party Classifier Testing.
----------------------------------------------------
This is where we specify all module variables and outward facing 
functions, i.e. functions that we may call from __main.py__ in the 
partycity package root folder.

Sreeraj Marar <sreerajm@umich.edu>
Rodney Shibu <rodneyss@umich.edu>
"""

import os
TESTING_DIR = os.path.dirname(__file__)

from partycity.testing.analyse import get_results
