# !/usr/bin/env python2.7
#
# feature_selection_tz.py -- This code is taken from the XBUS506
# feature_selection.ipynb notebook and converted for use with the
# Team Zero insideairbnb data.

# This file is designed to explore feature selection.

# 08/18/2016, Georgetown Data Science Cohort 6

from __future__ import print_function

import os
import zipfile
import requests
import pandas as pd


from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

# Read in the cleansed listing data from the file 'listings_clean.csv'
# This file must be stored in the working directory
listings_data = pd.read_csv('listings_clean.csv', sep = ',')
# Name the columns. I'm sure there's an easier way. The file
# 'listings_clean_headers.csv' includes the header names in the
# first row.

# We'll grab all the columns, including str types for now. There are 43 total

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Don't forget in the cleansed data has several columns where empty
# cells have been replaced with 0's (or other placeholder values)
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
listings_data.columns = [
    'id',
    'host_id',
    'host_name',
    'host_since',
    'host_response_rate',
    'host_acceptance_rate',
    'host_listings_count',
    'neighbourhood_cleansed',
    'state',
    'zipcode',
    'latitude',
    'longitude',
    'property_type',
    'room_type',
    'accommodates',
    'bathrooms',
    'bedrooms',
    'beds',
    'square_feet',
    'price',
    'weekly_price',
    'monthly_price',
    'security_deposit',
    'cleaning_fee',
    'guests_included',
    'extra_people',
    'minimum_nights',
    'maximum_nights',
    'availability_30',
    'availability_60',
    'availability_90',
    'availability_365',
    'number_of_reviews',
    'first_review',
    'last_review',
    'review_scores_rating',
    'review_scores_accuracy',
    'review_scores_cleanliness',
    'review_scores_checkin',
    'review_scores_communication',
    'review_scores_location',
    'review_scores_value',
    'reviews_per_month'
    ]

# Separate the dataframe into features and target(s). In this case
# we're going to set the target as price, since we're trying to predict
# price based on the most relevant instance features.

# We are only going to use int or float columns for now, not the str columns
# There are 34 columns in total now
features = listings_data[[
    'id',
    'host_id',
    # 'host_name',
    # 'host_since',
    'host_response_rate',
    'host_acceptance_rate',
    'host_listings_count',
    # 'neighbourhood_cleansed',
    # 'state',
    'zipcode',
    'latitude',
    'longitude',
    # 'property_type',
    # 'room_type',
    'accommodates',
    'bathrooms',
    'bedrooms',
    'beds',
    'square_feet',
    'weekly_price',
    'monthly_price',
    'security_deposit',
    'cleaning_fee',
    'guests_included',
    'extra_people',
    'minimum_nights',
    'maximum_nights',
    'availability_30',
    'availability_60',
    'availability_90',
    'availability_365',
    'number_of_reviews',
    # 'first_review',
    # 'last_review',
    'review_scores_rating',
    'review_scores_accuracy',
    'review_scores_cleanliness',
    'review_scores_checkin',
    'review_scores_communication',
    'review_scores_location',
    'review_scores_value',
    'reviews_per_month'
    ]]

labels = listings_data['price']

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# REGULARIZATION TECHNIQUES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Test first with LASSO
# model = Lasso()
# model.fit(features, labels)
# print(list(zip(features, model.coef_.tolist())))

# Next try Ridge
# model = Ridge()
# model.fit(features, labels)
# print(list(zip(features, model.coef_.tolist())))

# Finally, ElasticNet
# model = ElasticNet(l1_ratio = 0.5)
# model.fit(features, labels)
# print(list(zip(features, model.coef_.tolist())))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TRANSFORMER METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Now we'll grab the transformer code and wave our magic wand to select
# features based on the wisdom of Python
# For LASSO
# model = Lasso()
# sfm = SelectFromModel(model)
# sfm.fit(features, labels)
# print(list(features[sfm.get_support(indices=True)]))

# For Ridge
# model = Ridge()
# sfm = SelectFromModel(model)
# sfm.fit(features, labels)
# print(list(features[sfm.get_support(indices=True)]))

# For ElasticNet
# model = ElasticNet()
# sfm = SelectFromModel(model)
# sfm.fit(features, labels)
# print(list(features[sfm.get_support(indices=True)]))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DIMENSIONALITY REDUCTION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Grab the dimensionality reduction code, PCA and LCA

# PCA first
# pca = PCA(n_components=2)
# new_features = pca.fit(features).transform(features)
# print(new_features)

# LDA next
# lda = LDA(n_components=2)
# new_features = lda.fit(features, labels).transform(features)
# print(new_features)
