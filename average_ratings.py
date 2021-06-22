#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 07:38:25 2021

@author: firasfakih
"""

import pandas as pd
import sys
import difflib 


# importing data using pandas using tab as the delimeter
movie_titles = pd.read_csv(sys.argv[1], delimiter = "\t",names = ['title'])


# Import movie ratings data
movie_ratings = pd.read_csv(sys.argv[2])

# create a new column for entity resolved data
data = movie_ratings['title'].apply(difflib.get_close_matches,args=(movie_titles['title'],50))

# Change from list to string using explode:Method found on :https://stackoverflow.com/questions/60327204/converting-list-of-strings-in-pandas-column-into-string
df = data.explode().dropna()
df = df.astype(str)
df = df.groupby(level=0).agg(' '.join)


movie_ratings['title'] = df
movie_ratings = movie_ratings.dropna()

# find mean
output_df = movie_ratings.groupby(['title'], as_index = False).mean()
output_df['rating'] = round(output_df['rating'],2)


# TO csv
output_df.to_csv(sys.argv[3],index = False)
