import os
import json
import time
import pickle
import requests


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00236/seeds_dataset.txt"

def fetch_data(fname='seeds_dataset.txt'):
    """
    Helper method to retreive the ML Repository dataset.
    """
    response = requests.get(URL)
    print response

    outpath  = os.path.abspath(fname)
    with open(outpath, 'w') as f:
        f.write(str(response.content))

    return outpath

# Fetch the data if required
DATA = fetch_data()
