# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 15:28:42 2016

@author: Domenico
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

data = pd.read_csv("c:/Users/Domenico/Documents/team-zero/Data/listing/listings_clean_headers1.csv")
data.head()

# Create a histogram
fig = plt.figure()
ax = fig.add_subplot(111)
ax.hist(data['price'], bins = 200, range = (data['price'].min(),data['price'].max()))
plt.title('Price per Review')
plt.xlabel('price')
plt.ylabel('number_of_reviews')
plt.show()

sns.distplot(data['weekly_price'], bins = 50)
sns.distplot(data['price'], bins = 50)

# Create a violin
g = sns.factorplot(x="neighbourhood_cleansed", y="price", hue = "room_type", 
                   data=data[data.price.notnull()], 
                             kind="violin")
# factorplot

g = sns.factorplot("price", col="room_type", col_wrap=4, 
                   data=data[data.room_type.notnull()], kind="count", size=4, aspect=.8)

# Draw a nested barplot
g = sns.factorplot(x="minimum_nights", 
                   y="price", 
                   hue="room_type", 
                   data=data,
                   size=6, kind="bar", palette="muted")
g.despine(left=True)
g.set_ylabels("NOT SURE YET")                   

#pairplot
g = sns.pairplot(data=data[['host_response_rate', 'host_acceptance_rate', 'host_listings_count', 'price', 'beds', 'accommodates', 'minimum_nights', 'maximum_nights', 'bathrooms']], hue='price', dropna=True)    


#Jointplot
g = sns.jointplot("number_of_reviews", "price", data)

g = sns.jointplot("price", "host_listings_count", data)

g = sns.jointplot("price", "accommodates", data)

g = sns.jointplot("price", "beds", data)

g = sns.jointplot("price", "review_scores_rating", data)

g = sns.jointplot("price", "review_scores_value", data)

g = sns.jointplot("price", "cleaning_fee", data)

g = sns.jointplot("host_acceptance_rate", "price", data)

g = sns.jointplot("availability_30", "price", data)