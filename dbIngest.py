import pandas as pd
from sqlalchemy import create_engine
import psycopg2
engine = create_engine('postgresql://Devin:b7410b@localhost:5432/reviews')

df = pd.read_csv('/Users/Devin/Repos/Georgetown/TZ/reviews 2.csv')
df.to_sql("reviews", engine)
