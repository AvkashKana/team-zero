import pandas as pd
from sqlalchemy import create_engine
import psycopg2

engine = create_engine('postgresql+psycopg2://teamzero:123456@localhost:5432/teamzeroDB')

df = pd.read_csv('/Users/Devin/Repos/Georgetown/TZ/reviews 2.csv')
df.to_sql("reviews", engine, if_exists='replace')

df = pd.read_csv('/Users/Devin/Repos/Georgetown/TZ/neighbourhoods.csv')
df.to_sql("neighborhoods", engine, if_exists='replace')

df = pd.read_csv('/Users/Devin/Repos/Georgetown/TZ/listings.csv')
df.to_sql("listings", engine, if_exists='replace')

df = pd.read_csv('/Users/Devin/Repos/Georgetown/TZ/calendar.csv')
df.to_sql("calendar", engine, if_exists='replace')
