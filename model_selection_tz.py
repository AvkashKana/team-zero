# !/usr/bin/env python2.7
#
# model_selection_tz.py -- This code is taken from the XBUS506
# model_selection.ipynb notebook and converted for use with the
# Team Zero insideairbnb data.

# This file is designed to explore machine learning models.

# 08/22/2016, Georgetown Data Science Cohort 6

import json
import os
import pickle
import requests
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.cross_validation import KFold, StratifiedKFold, train_test_split
from sklearn.datasets.base import Bunch
from sklearn.ensemble import BaggingClassifier, ExtraTreesClassifier, RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import ElasticNetCV, LogisticRegressionCV, LogisticRegression, SGDClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, auc, roc_curve, roc_auc_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.svm import LinearSVC, NuSVC, SVC

# Create a list of names, drawn from the header for each feature. In this case
# we're going to use a mix of features identified by the Ridge and ElasticNet
# transformer code in feature_selection_tz.py
names = [
    'host_response_rate',
    'host_acceptance_rate',
    'latitude',
    'longitude',
    'property_type',
    'room_type',
    'accommodates',
    'bathrooms',
    'bedrooms',
    'beds',
    'price',
    'review_scores_communication',
    'review_scores_location',
    'reviews_per_month'
]

# Create the data frame using the relevant columns from the listings_clean.csv
# file. In this case be sure to confirm you are pulling all the relevant rows by
# explicitly indicating there are no column headers
data = pd.read_csv('listings_clean.csv',
            header = None,
            usecols = [
            4, 5, 10, 11,
            12, 13, 14, 15,
            16, 17, 19, 39, 40, 42
            ])

# Add the column headers using the names list
data.columns = names

# print (data.head())

# Creat the meta.json file, similar to the census and model_selection notebooks.
# Here we'll use price as the target - we shouldn't need to limit ourselves to
# unique values of price (?).

# We'll also convert the categorial columns to values

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! FIXED 8/26/16 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Listing ID 3771 has a property type that is empty, which will cause the
# corresponding meta.json list to include a NaN value
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! FIXED 8/26/16 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Replaced the empty property type list element with 'Apartment'
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! FIXED 8/26/16 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

meta = {
    'target_names' : list(data.price),
    'feature_names' : list(data.columns),
    'categorical_features' : {
        column : list(data[column].unique())
        for column in data.columns
        if data[column].dtype == 'object'
    },
}

#Write the meta.json file
with open('meta.json', 'w') as f:
    json.dump(meta, f, indent = 2)

# Per the model_selection.ipynb file, load the data and create the bunch
def load_data():
    # Load meta data from the json created just above
    with open('meta.json', 'r') as f:
        meta = json.load(f)

    names = meta['feature_names']

    # Load the readme.md info
    with open('README.md', 'r') as f:
        readme = f.read()

    # Load the data. This is duplicative, but just to be explicit
    # listings = pd.read_csv('listings_clean_headers.csv', names = names)
    # print (data[names[0:]])

    # Remove target from feature_names
    meta['feature_names'].pop(10)

    # Return the bunch
    return Bunch(
        data = data[names[0:]],
        target = data.price,
        target_names = meta['target_names'],
        feature_names = meta['feature_names'],
        categorical_features = meta['categorical_features'],
        DESCR = readme
    )

dataset = load_data()
