# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 20:34:20 2016

@author: Domenico
"""

#How to Select Features for Machine Learning (Jupyter Notebook feature_selection)

#Imports
from __future__ import print_function

%matplotlib inline

import os
import zipfile
import requests
import pandas as pd
import json
import time
import pickle
import requests
import gzip

from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Fetch The Data option1 (ONLY RUN 1 OPTION)
listing = ('http://data.insideairbnb.com/united-states/dc/washington-dc/2015-10-03/data', 'listings.csv.gz')
def download_data(url, name, path='data'):
    if not os.path.exists(path):
        os.mkdir(path)

    response = requests.get(url)
    with gzip.open(os.path.join(path, name), 'wb') as f:
        reader = csv.reader(f)
   # with open(os.path.join(path, name), 'wb') as f:
        f.write(response.content)
        
def download_all(path='data'):
    for href, name in (listing):
        download_data(href, name, path)

    # Extract the listing zip data
    z = zipfile.ZipFile(os.path.join(path, 'listings.csv.gz'))
    z.extractall(os.path.join(path, 'listing'))

path='data'
download_all(path)

#Fetch The Data option2 (ONLY RUN 1 OPTION)
URL = "http://data.insideairbnb.com/united-states/dc/washington-dc/2015-10-03/data/listings.csv.gz"

def fetch_data(fname='listings.csv.gz'):
    """
    Helper method to retreive the ML Repository dataset.
    """
    response = requests.get(URL)
    outpath  = os.path.abspath(fname)
    with gzip.open(os.path.join(path, name), 'wb') as f:
        reader = csv.reader(f)
        f.write(response.content)
    
    return outpath

# Fetch the data if required
DATA = fetch_data()

#Fetch The Data option3 (ONLY RUN 1 OPTION)
listing = pd.read_csv("c:/Users/Domenico/Documents/team-zero/Data/listing/listings_clean_headers1.csv")
listing.head()
metro = pd.read_csv("c:/Users/Domenico/Documents/team-zero/Data/listing/Metro_Stations_District. Data sourcecsv.csv")
metro.head()

#Code to Cleanse Dataset


#Load the first dataset into a dataframe
listing.dataframe = listing [[
    'id', 'accommodates', 'host_response_rate', 'host_acceptance_rate', 'host_listings_count', 'bathrooms', 'bedrooms',
    'beds', 'square_feet', 'price', 'security_deposit', 'cleaning_fee', 'guests_included', 'extra_people', 'minimum_nights',
    'number_of_reviews', 'maximum_nights', 'availability_30', 'availability_60', 'availability_90', 'availability_365'
]]

listing.dataframe.describe()

features = listing[['accommodates', 'host_response_rate', 'host_acceptance_rate', 'host_listings_count', 'number_of_reviews']]
labels   = listing['price']

list(features)

#Regularization techniques

#LASSO (L1 Regularization)
#LASSO forces weak features to have zeroes as coefficients, effectively dropping the least predictive features

model = Lasso()
model.fit(features, labels)
print(list(zip(features, model.coef_.tolist())))

#Ridge Regression (L2 Regularization)
#Ridge assigns every feature a weight, but spreads the coefficient values out more equally, shrinking but still maintaining less predictive features.

model = Ridge()
model.fit(features, labels)
print(list(zip(features, model.coef_.tolist())))

#ElasticNet
#ElasticNet is a linear combination of L1 and L2 regularization, meaning it combines Ridge and LASSO and essentially splits the difference.
model = ElasticNet(l1_ratio=0.10)
model.fit(features, labels)
print(list(zip(features, model.coef_.tolist())))

#Transformer methods
#SelectFromModel()
#Scikit-Learn has a meta-transformer method for selecting features based on importance weights

model = Lasso()
sfm = SelectFromModel(model)
sfm.fit(features, labels)
print(list(features[sfm.get_support(indices=True)]))

model = Ridge()
sfm = SelectFromModel(model)
sfm.fit(features, labels)
print(list(features[sfm.get_support(indices=True)]))

model = ElasticNet()
sfm = SelectFromModel(model)
sfm.fit(features, labels)
print(list(features[sfm.get_support(indices=True)]))

#Dimensionality reduction
#Principal component analysis (PCA)
#Linear dimensionality reduction using Singular Value Decomposition (SVD) of the data and keeping only the most significant singular vectors to project the data into a lower dimensional space.
#•Unsupervised method
#•Uses a signal representation criterion
#•Identifies the combination of attributes that account for the most variance in the data.

pca = PCA(n_components=2)
new_features = pca.fit(features).transform(features)
print(new_features)

#Linear discriminant analysis (LDA)
#A classifier with a linear decision boundary, generated by fitting class conditional densities to the data and using Bayes’ rule. The model fits a Gaussian density to each class, assuming that all classes share the same covariance matrix. Can be used to reduce the dimensionality of the input by projecting it to the most discriminative directions.
#•Supervised method
#•Uses a classification criterion
#•Tries to identify attributes that account for the most variance between classes

lda = LDA(n_components=2)
new_features = lda.fit(features, labels).transform(features)
print(new_features)







