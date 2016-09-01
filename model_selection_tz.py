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

# Transform categorical data from object type into numeric type
class EncodeCategorical(BaseEstimator, TransformerMixin):
    """
    Encodes a specified list of columns or all columns if None.
    """

    def __init__(self, columns=None):
        self.columns  = columns
        self.encoders = None

    def fit(self, data, target=None):
        """
        Expects a data frame with named columns to encode.
        """
        # Encode all columns if columns is None
        if self.columns is None:
            self.columns = data.columns

        # Fit a label encoder for each column in the data frame
        self.encoders = {
            column: LabelEncoder().fit(data[column])
            for column in self.columns
        }
        return self

    def transform(self, data):
        """
        Uses the encoders to transform a data frame.
        """
        output = data.copy()
        for column, encoder in self.encoders.items():
            output[column] = encoder.transform(data[column])

        return output

# Establish output directory
# FIX LATER: WHY DOES THE os.mkdir LINE NOT WORK WHEN THE DIRECTORY DOESN'T
# ALREADY EXIST?
if not os.path.exists(os.path.join('data', 'listings', 'output')):
    os.mkdir(os.path.join(os.getcwd(), 'data', 'listings', 'output'))

OUTPATH = os.path.abspath(os.path.join('.', 'data', 'listings', 'output'))
print OUTPATH

# Meat and potatoes model selection code
def model_selection(dataset, feature_model, model_estimator, fse_label, model_label):

    """
    Test various combinations of estimators for feature selection and modeling.
    The pipeline generates the dataset, encodes columns, then uses the encoded results for feature selection.
    Finally,the selected features are sent to the estimator model for scoring.
    """

    start  = time.time()

    # assign X
    X = dataset.data
    # assign y, encoding the target value
    y = LabelEncoder().fit_transform(dataset.target)

    if feature_model == 'none':
        # use the pipeline that does not use SelectFromModel
        model = Pipeline([
                 ('label_encoding', EncodeCategorical(dataset.categorical_features.keys())),
                 ('one_hot_encoder', OneHotEncoder()),
                 ('estimator', model_estimator)
            ])
    else:
        #use the pipeline that has SelectFromModel
        model = Pipeline([
                         ('label_encoding', EncodeCategorical()),
                         ('one_hot_encoder', OneHotEncoder()),
                         ('estimator', model_estimator),
                         ('feature_selection', SelectFromModel(feature_model)),
                         ('estimator', model_estimator)
                          ])

    """
    Train and test the model using StratifiedKFold cross validation. Compile the scores for each iteration of the model.
    """
    scores = {'accuracy':[], 'auc':[], 'f1':[], 'precision':[], 'recall':[]}

    # Kick it up a notch! 12 folds
    for train, test in StratifiedKFold(y, n_folds=12, shuffle=True):  # Ben says always use 12 folds! We cheat a bit here...
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

        model.fit(X_train, y_train)
        expected  = y_test
        predicted = model.predict(X_test)

        ## Visualize scores
        fpr, tpr, thresholds = roc_curve(expected, predicted)
        roc_auc = auc(fpr, tpr)
        plt.figure()
        plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC-AUC for {}'.format(model_label))
        plt.legend(loc="lower right")
        plt.show()

        ## Record scores
        scores['accuracy'].append(accuracy_score(expected, predicted))
        scores['f1'].append(f1_score(expected, predicted, average='binary'))
        scores['precision'].append(precision_score(expected, predicted, average='binary'))
        scores['recall'].append(recall_score(expected, predicted, average='binary'))

        """
        AUC cannot be computed if only 1 class is represented in the data. When that happens, record an AUC score of 0.
        """
        try:
            scores['auc'].append(roc_auc_score(expected, predicted))
        except:
            scores['auc'].append(0)

    """
    Print the modeling details and the mean score.
    """
    print "\nBuild and Validation of took {:0.3f} seconds\n".format(time.time()-start)
    print "Feature Selection Estimator: {}\n".format(fse_label)
    print "Estimator Model: {}\n".format(model_label)
    print "Validation scores are as follows:\n"
    print pd.DataFrame(scores).mean()

    """
    Create a data frame with the mean score and estimator details.
    """
    df = pd.DataFrame(scores).mean()
    df['SelectFromModel'] =  fse_label
    df['Estimator']  = model_label

    """
    Write official estimator to disk
    """
    estimator = model
    estimator.fit(X,y)

    pickle_path = os.path.join(OUTPATH + "/", fse_label.lower().replace(" ", "-") + "_" + model_label.lower().replace(" ", "-") + ".pickle")
    with open(pickle_path, 'w') as f:
        pickle.dump(estimator, f)

    print "\nFitted model written to:\n{}".format(os.path.abspath(pickle_path))

    return df

# Evaluate the models
evaluation = pd.DataFrame()

evaluation = evaluation.append(pd.DataFrame(model_selection(dataset, "none", LogisticRegression(), "none", "LogisticRegression")).T)
# evaluation = evaluation.append(pd.DataFrame(model_selection(dataset, "none", KNeighborsClassifier(), "none", "KNeighborsClassifier")).T)
# evaluation = evaluation.append(pd.DataFrame(model_selection(dataset, "none", BaggingClassifier(KNeighborsClassifier()), "none", "BaggedKNeighborsClassifier")).T)
# evaluation = evaluation.append(pd.DataFrame(model_selection(dataset, "none", RandomForestClassifier(), "none", "RandomForestClassifier")).T)
# evaluation = evaluation.append(pd.DataFrame(model_selection(dataset, "none", ExtraTreesClassifier(), "none", "ExtraTreesClassifier")).T)
# evaluation = evaluation.append(pd.DataFrame(model_selection(dataset, "none", SGDClassifier(), "none", "SGDClassifier")).T)
# evaluation = evaluation.append(pd.DataFrame(model_selection(dataset, "none", LinearSVC(), "none", "LinearSVC")).T)
#
# evaluation.to_csv(os.path.join('data', 'listings', 'model_comparison.csv'), index=False)
