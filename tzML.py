import os
import json
import time
import pickle
import requests

from sys import exit

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00236/seeds_dataset.txt"
#
# def fetch_data(fname='seeds_dataset.txt'):
#     """
#     Helper method to retreive the ML Repository dataset.
#     """
#     response = requests.get(URL)
#     outpath  = os.path.abspath(fname)
#     with open(outpath, 'w') as f:
#         f.write(str(response.content))
#
#     return outpath

# Fetch the data if required
DATA = os.path.abspath('listings.csv')

FEATURES  = [
    "id",
    "listing_url",
    "id",
    "listing_url",
    "scrape_id",
    "last_scraped,"
    "name",
    "summary",
    "space",
    "description",
    "experiences_offered",
    "neighborhood_overview",
    "notes",
    "transit",
    "thumbnail_url",
    "medium_url",
    "picture_url",
    "xl_picture_url",
    "host_id",
    "host_url",
    "host_name",
    "host_since",
    "host_location",
    "host_about",
    "host_response_time",
    "host_response_rate",
    "host_acceptance_rate",
    "host_is_superhost",
    "host_thumbnail_url",
    "host_picture_url",
    "host_neighbourhood",
    "host_listings_count",
    "host_total_listings_count",
    "host_verifications",
    "host_has_profile_pic",
    "host_identity_verified",
    "street",
    "neighbourhood",
    "neighbourhood_cleansed",
    "neighbourhood_group_cleansed",
    "city",
    "state",
    "zipcode",
    "market",
    "smart_location",
    "country_code",
    "country",
    "latitude",
    "longitude",
    "is_location_exact",
    "property_type",
    "room_type",
    "accommodates",
    "bathrooms",
    "bedrooms",
    "beds",
    "bed_type",
    "amenities",
    "square_feet",
    "price",
    "weekly_price",
    "monthly_price",
    "security_deposit",
    "cleaning_fee",
    "guests_included",
    "extra_people",
    "minimum_nights",
    "maximum_nights",
    "calendar_updated",
    "has_availability",
    "availability_30",
    "availability_60",
    "availability_90",
    "availability_365",
    "calendar_last_scraped",
    "number_of_reviews",
    "first_review",
    "last_review",
    "review_scores_rating",
    "review_scores_accuracy",
    "review_scores_cleanliness",
    "review_scores_checkin",
    "review_scores_communication",
    "review_scores_location",
    "review_scores_value",
    "requires_license",
    "license",
    "jurisdiction_names",
    "instant_bookable",
    "cancellation_policy",
    "require_guest_profile_picture",
    "require_guest_phone_verification",
    "calculated_host_listings_count",
    "reviews_per_month"
]

# LABEL_MAP = {
#     1: "Kama",
#     2: "Rosa",
#     3: "Canadian",
# }

# Read the data into a DataFrame
df = pd.read_csv(DATA, sep=',', names=FEATURES)

# Convert class labels into text
# for k,v in LABEL_MAP.items():
#     df.ix[df.label == k, 'label'] = v

# Describe the dataset
print df.describe()
