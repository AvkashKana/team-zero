# !/usr/bin/env python2.7
#
# vizTest.py -- Exploring visualizatons based
# on XBUS506 workshop materials.

# 08/06/2016, Georgetown Data Science Cohort 6

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

df = pd.read_csv('listings_clean.csv')

print df.head()
