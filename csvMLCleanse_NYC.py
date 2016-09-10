# !/usr/bin/env python2.7
#
# csvMLCleanse_NYC.py -- Extracts and cleanses
# key columns from the listing.csv data file.
# The really, really hard way. Pain train.

# This is to cleanse NYC data for testing model predictions.

# This script only needs to be run once.

# 08/06/2016, Georgetown Data Science Cohort 6

import csv
import re
from itertools import izip

# Open the listings file as downloaded from insideairbnb.com
# File needs to be stored in the working directory
listings = open('nyc_listings.csv')
listingReader = csv.reader(listings)
listingData = list(listingReader)

# Create a list for each feature/column we want to cleanse
l_ID = []
host_ID = []
host_name = []
host_since = []
host_RR = []
host_AR = []
host_LC = []
neigh_C = []
state = []
zip_code = []
lat = []
longitude = []
prop_type = []
room_type = []
accom = []
bath = []
bedrooms = []
beds = []
sq_ft = []
price = []
week_price = []
month_price = []
sec_deposit = []
cleaning_fee = []
guest_inc = []
extra_peop = []
min_night = []
max_night = []
avail_30 = []
avail_60 = []
avail_90 = []
avail_365 = []
number_reviews = []
f_review = []
l_review = []
review_score = []
review_score_acc = []
review_score_clean = []
review_score_checkin = []
review_score_comm = []
review_score_loc = []
review_score_value = []
review_permonth = []

# Populate each list from the appropriate column
for i in range (1,38811):
    l_ID.append(listingData[i][0])
    host_ID.append(listingData[i][16])
    host_name.append(listingData[i][18])
    host_since.append(listingData[i][19])
    host_RR.append(listingData[i][23])
    host_AR.append(listingData[i][24])
    host_LC.append(listingData[i][29])
    neigh_C.append(listingData[i][36])
    state.append(listingData[i][39])
    zip_code.append(listingData[i][40])
    lat.append(listingData[i][45])
    longitude.append(listingData[i][46])
    prop_type.append(listingData[i][48])
    room_type.append(listingData[i][49])
    accom.append(listingData[i][50])
    bath.append(listingData[i][51])
    bedrooms.append(listingData[i][52])
    beds.append(listingData[i][53])
    sq_ft.append(listingData[i][56])
    price.append(listingData[i][57])
    week_price.append(listingData[i][58])
    month_price.append(listingData[i][59])
    sec_deposit.append(listingData[i][60])
    cleaning_fee.append(listingData[i][61])
    guest_inc.append(listingData[i][62])
    extra_peop.append(listingData[i][63])
    min_night.append(listingData[i][64])
    max_night.append(listingData[i][65])
    avail_30.append(listingData[i][68])
    avail_60.append(listingData[i][69])
    avail_90.append(listingData[i][70])
    avail_365.append(listingData[i][71])
    number_reviews.append(listingData[i][73])
    f_review.append(listingData[i][74])
    l_review.append(listingData[i][75])
    review_score.append(listingData[i][76])
    review_score_acc.append(listingData[i][77])
    review_score_clean.append(listingData[i][78])
    review_score_checkin.append(listingData[i][79])
    review_score_comm.append(listingData[i][80])
    review_score_loc.append(listingData[i][81])
    review_score_value.append(listingData[i][82])
    review_permonth.append(listingData[i][91])

# Convert listing ID from string to int
l_ID = [int(i) for i in l_ID]
# Convert host ID from string to int
host_ID = [int(i) for i in host_ID]
# Leave host name as string for now
host_name = host_name
# Leave host_since as string for now, this is a date YYYY-MM-DD
host_since = host_since
# Host response rate is a percentage. First strip the '%' character,
# then replace instances of N/A with 0 (this may/may not throw off further
# analysis), convert to float, and divide by 100 to give a decimal value
host_RR = [i.rstrip('%') for i in host_RR]
host_RR = [i.replace('N/A', '0') for i in host_RR]
host_RR = [float(i) for i in host_RR]
host_RR = [i/100 for i in host_RR]
# Perform the same transformations to host acceptance rate as to host_RR
# We still have the same problem where we replace N/A with 0
host_AR = [i.rstrip('%') for i in host_AR]
host_AR = [i.replace('N/A', '0') for i in host_AR]
host_AR = [float(i) for i in host_AR]
host_AR = [i/100 for i in host_AR]
# Convert host listing count to int
host_LC = [int(i) for i in host_LC]
# Neighborhood cleansed can be left as a str for now. We'll need to match this
# to the neighborhood coordinates later
neigh_C = neigh_C
# State can stay as str
state = state
# There are several zip codes in the zip+4 (XXXXX-XXXX) format. First, grab
# only the five number primary zip code. Then replace missing zip codes
# with 00000 (Nowheresville, USA)
zip_code = [i[:5] for i in zip_code]
zip_code = [(int(i) if i else '00000') for i in zip_code]
zip_code = [int(i) for i in zip_code]
# Latitude gets converted to a float
lat = [float(i) for i in lat]
# Longitude gets converted to a float
longitude = [float(i) for i in longitude]
# Property type can remain as a string
# ID 3771 has no property type. Because the overall listing population is
# 61% apartments, and it's not clearly some other property type,
# we'll simply guess that it's an apartment by replacing empty values with
# 'Apartment'
prop_type = [(i if i else 'Apartment') for i in prop_type]
# Room type can remain as a string
room_type = room_type
# Accommodates gets converted to an int
accom = [int(i) for i in accom]
# Bath gets converted to an int, empty cells replaced with 0
bath = [(float(i) if i else '0') for i in bath]
bath = [float(i) for i in bath]
# Bedrooms gets converted to an int. Empty cells replaced
# with 0
bedrooms = [(int(i) if i else '0') for i in bedrooms]
bedrooms = [int(i) for i in bedrooms]
# Beds gets converted to an int, empty cells replaced with 0
beds = [(int(i) if i else '0') for i in beds]
beds = [int(i) for i in beds]
# Square feet gets converted to a float, empty cells are
# replaced with 0.  However, because there are only 82
# values total and only 74 non-zero values, the 0 replacements
# should likely be excluded and/or adjusted.
sq_ft = [(float(i) if i else '0') for i in sq_ft]
sq_ft = [float(i) for i in sq_ft]
# Price gets covnerted to a float. First, remove the '$'
# symbol, then remove the ',' marks, then convert to float
price = [i.lstrip('$') for i in price]
price = [i.replace(',','') for i in price]
price = [float(i) for i in price]
# Weekly price gets the same treatment as price. Empty cells
# are replaced with '0'
week_price = [i.lstrip('$') for i in week_price]
week_price = [i.replace(',','') for i in week_price]
week_price = [(float(i) if i else '0') for i in week_price]
week_price = [float(i) for i in week_price]
# Monthly price gets the same treatment as weekly price
month_price = [i.lstrip('$') for i in month_price]
month_price = [i.replace(',','') for i in month_price]
month_price = [(float(i) if i else '0') for i in month_price]
month_price = [float(i) for i in month_price]
# Security deposit gets the same as monthly and weekly price
sec_deposit = [i.lstrip('$') for i in sec_deposit]
sec_deposit = [i.replace(',','') for i in sec_deposit]
sec_deposit = [(float(i) if i else '0') for i in sec_deposit]
sec_deposit = [float(i) for i in sec_deposit]
# Cleaning fee gets the same treatment as security deposit,
# monthly price, and weekly price.
cleaning_fee = [i.lstrip('$') for i in cleaning_fee]
cleaning_fee = [i.replace(',','') for i in cleaning_fee]
cleaning_fee = [(float(i) if i else '0') for i in cleaning_fee]
cleaning_fee = [float(i) for i in cleaning_fee]
# Guests included gets converted to an int
guest_inc = [int(i) for i in guest_inc]
# Extra people gets the same treatment as price
extra_peop = [i.lstrip('$') for i in extra_peop]
extra_peop = [i.replace(',','') for i in extra_peop]
extra_peop = [float(i) for i in extra_peop]
# Minimum nights gets converted to an int
min_night = [int(i) for i in min_night]
# Maximum nights gets converted to an int
max_night = [int(i) for i in max_night]
# 30 day availability gets converted to an int
avail_30 = [int(i) for i in avail_30]
# 60 day availability gets converted to an int
avail_60 = [int(i) for i in avail_60]
# 90 day availability gets converted to an int
avail_90 = [int(i) for i in avail_90]
# 365 day availability gets covnerted to an int
avail_365 = [int(i) for i in avail_365]
# Number of reviews gets converted to an int
number_reviews = [int(i) for i in number_reviews]
# First review stays as a string.
f_review = f_review
# Last review stays as a string.
l_review = l_review
# Review scores rating gets convert to an int.
# Empty cells are replaced with 0. They should
# probably be ignored in any calculations.
review_score = [(int(i) if i else '0') for i in review_score]
review_score = [int(i) for i in review_score]
# Review scores accuracy gets the same treatment
# as review scores review scores rating
review_score_acc = [(int(i) if i else '0') for i in review_score_acc]
review_score_acc = [int(i) for i in review_score_acc]
# Review scores cleanliness gets the same treatment
# as review scores rating and accuracy
review_score_clean = [(int(i) if i else '0') for i in review_score_clean]
review_score_clean = [int(i) for i in review_score_clean]
# Review scores checkin gets the same treatment as the others
review_score_checkin = [(int(i) if i else '0') for i in review_score_checkin]
review_score_checkin = [int(i) for i in review_score_checkin]
# Review scores communication gets the same treatment as others
review_score_comm = [(int(i) if i else '0') for i in review_score_comm]
review_score_comm = [int(i) for i in review_score_comm]
# Review scores location gets the same treatment as others
review_score_loc = [(int(i) if i else '0') for i in review_score_loc]
review_score_loc = [int(i) for i in review_score_loc]
# Review scores value gets the same treatment as others
review_score_value = [(int(i) if i else '0') for i in review_score_value]
review_score_value = [int(i) for i in review_score_value]
# Reviews per month gets converted to a float. Empty cells are
# replaced with '0'
review_permonth = [(float(i) if i else '0') for i in review_permonth]
review_permonth = [float(i) for i in review_permonth]

# Check you're getting the output you want
# print review_permonth[1]
# print type(review_permonth[1])

# Write all these rows to a CSV name 'listings_clean.csv' stored in the
# working directory
with open('nyc_listings_clean.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(izip(l_ID,
    host_ID,
    host_name,
    host_since,
    host_RR,
    host_AR,
    host_LC,
    neigh_C,
    state,
    zip_code,
    lat,
    longitude,
    prop_type,
    room_type,
    accom,
    bath,
    bedrooms,
    beds,
    sq_ft,
    price,
    week_price,
    month_price,
    sec_deposit,
    cleaning_fee,
    guest_inc,
    extra_peop,
    min_night,
    max_night,
    avail_30,
    avail_60,
    avail_90,
    avail_365,
    number_reviews,
    f_review,
    l_review,
    review_score,
    review_score_acc,
    review_score_clean,
    review_score_checkin,
    review_score_comm,
    review_score_loc,
    review_score_value,
    review_permonth,
    ))

# print('The median accommodation number is ' + str(statistics.median(listingAccom)))
#
# listingDataPrice = [i.lstrip('$') for i in listingDataPrice]
# listingDataPrice = [i.replace(',','') for i in listingDataPrice]
# listingDataPrice = [float(i) for i in listingDataPrice]
#
# print('The median listing price is $' + str(statistics.median(listingDataPrice)))
