# usr/bin/evn python2.7
#
# dbIngest.py -- This script will create several PostgreSQL
# tables from the baseline Insideairbnb.com baseline CSV files


import pandas as pd
from sqlalchemy import create_engine
import psycopg2

# Creating a sqlalchemy engine connected to the local database,
# 'teamzeroDB'.
# The database and login role must already exist before running
# the script.

# In this case I'm using the login role 'teamzero' with
# a throwaway password, '123456'. My PostgreSQL server is listening
# on the default port, 5432.

engine = create_engine('postgresql+psycopg2://teamzero:123456@localhost:5432/teamzeroDB')

# Read the CSV files and then write them to a new table in the db.

# WARNING!! This is set to replace the table if it already exists,
# This code might wreck your existing tables.

df = pd.read_csv('/Users/Devin/Repos/Georgetown/TZ/reviews 2.csv')
df.to_sql("reviews", engine, if_exists='replace')

df = pd.read_csv('/Users/Devin/Repos/Georgetown/TZ/neighbourhoods.csv')
df.to_sql("neighborhoods", engine, if_exists='replace')

df = pd.read_csv('/Users/Devin/Repos/Georgetown/TZ/listings.csv')
df.to_sql("listings", engine, if_exists='replace')

df = pd.read_csv('/Users/Devin/Repos/Georgetown/TZ/calendar.csv')
df.to_sql("calendar", engine, if_exists='replace')
