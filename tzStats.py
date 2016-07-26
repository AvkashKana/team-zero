# !/usr/bin/env python2.7
#
# tzStats.py -- Connects to PostgreSQL database
# containing listing data and performs basic stats
# operations to confirm the data is good and explore
# its contours.

# 07/25/2016, Georgetown Data Science Cohort 6

import psycopg2

# Connect to the Team Zero database, 'teamzeroDB', hosted locally.
# In this case I'm using my local login role, 'Devin', with a
# throwaway password, '123456'
#

try:
    conn = psycopg2.connect("dbname = teamzeroDB user = Devin host = localhost password = 123456")
except:
    print "Cannot connect to the database"

# Define a cursor to perform db operations
cur = conn.cursor()

# Select and print the neighbourhood column from the neighborhoods table
# Watch the spelling on neighborhood/neighbourhood

cur.execute("SELECT neighbourhood FROM neighborhoods;")

neighborRows = cur.fetchall()

print "\nShow me the neighborhoods in the table:\n"
for row in neighborRows:
    print " ", row[0]
