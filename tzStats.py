# !/usr/bin/env python2.7
#
# tzStats.py -- Connects to PostgreSQL database
# containing listing data then performs basic stats
# operations to confirm the data is good and explore
# its contours.

# 07/25/2016, Georgetown Data Science Cohort 6

import psycopg2, statistics, os, csv
import pandas as pd
from itertools import chain
from sys import exit

# If you are running this code with the Team Zero CSV files
# stored in the current working directory, uncomment and run the
# code between lines 24 and 40 to load the CSV file 'listings.csv'
# and then calculate the median listing price
#
# def read_lines():
#     with open('listings.csv', 'rU') as data:
#         reader = csv.reader(data)
#         for row in reader:
#             yield [ float(i) for i in row ]
#
# listings = open('listings.csv')
# listingReader = csv.reader(listings)
# listingData = list(listingReader)
#
# listingDataPrice = []
# listingAccom = []
#
# for i in range (1,3724):
#     listingDataPrice.append(listingData[i][57])
#     listingAccom.append(listingData[i][50])
#
# print('The median accommodation number is ' + str(statistics.median(listingAccom)))
#
# listingDataPrice = [i.lstrip('$') for i in listingDataPrice]
# listingDataPrice = [i.replace(',','') for i in listingDataPrice]
# listingDataPrice = [float(i) for i in listingDataPrice]
#
# print('The median listing price is $' + str(statistics.median(listingDataPrice)))
#
# exit(0)

# Connect to the Team Zero database, 'teamzeroDB', hosted locally.
# In this case I'm using my local login role, 'Devin', with a
# throwaway password, '123456'

try:
    conn = psycopg2.connect("dbname = teamzeroDB user = Devin host = localhost password = 123456")
except:
    print "Cannot connect to the database"

# Define a cursor to perform db operations
cur = conn.cursor()

# Select and print the neighbourhood column from the neighborhoods table
# Watch the spelling on neighborhood/neighbourhood

# cur.execute("SELECT listings FROM neighborhoods;")
#
# neighborRows = cur.fetchall()
#
# print "\nShow me the neighborhoods in the table:\n"
# for row in neighborRows:
#     print " ", row[0]

# Select 'price' column from the 'listings' table and calculate
# mean and median price

cur.execute("SELECT price FROM listings;")
price = cur.fetchall()

# Since the prior operation returns a list of tuples,
# i.e., [(1,), (2,)], need to convert to a list of strings
price = list(chain.from_iterable(price))

# Convert the list of strings just created to a list of
# integers, accounting for the leading $ symbol and also
# removing commas, e.g., '$1,000.00' becomes 1000.00
price = [i.lstrip('$') for i in price]
price = [i.replace(',', '') for i in price]
price = [float(i) for i in price]

# Calculate and print the median using the statistics module
print('The median listing price is $' + str(statistics.median(price)))

# Double check the calculated median using a function
def median(lst):
    sortedLst = sorted(lst)
    lstLen = len(lst)
    index = (lstLen - 1) // 2

    if (lstLen % 2):
        return sortedLst[index]
    else:
        return (sortedLst[index] + sortedLst[index + 1])/2.0

print('Calculated another way, the median listing price is $' + str(median(price)))
print('The total number of listing records is ' + str(len(price)))
