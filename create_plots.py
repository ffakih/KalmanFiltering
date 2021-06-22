import sys
import pandas as pd
import matplotlib.pyplot as plt

filename1 = sys.argv[1]
filename2 = sys.argv[2]


# Read in both csv files and separate them into two data frames
data1 = pd.read_csv(filename1,sep=' ',header = None, index_col = 1, names=['lang','page','views','bytes'])
data2 = pd.read_csv(filename2,sep=' ',header = None, index_col = 1, names=['lang','page','views','bytes'])

# Sorting by views in descending order
data1 = data1.sort_values(by='views',axis = 0, ascending = False)

# Plot 1

plt.figure(figsize=(10, 5)) # change the size to something sensible
plt.subplot(1, 2, 1) # subplots in 1 row, 2 columns, select the first
plt.plot(data1['views'].values,data = data1) # build plot 1
plt.ylabel('Views')
plt.xlabel('Rank')
plt.title('Popularity Distribution')


# Plot 2

# adding both views series to one dataframe

data1['views2'] = data2['views']


plt.subplot(1, 2, 2) # ... and then select the second
plt.xscale('log')
plt.yscale('log')
plt.plot(data1['views'].values, data1['views2'].values,'bo') # build plot
plt.xlabel('Hour 1 views')
plt.ylabel('Hour 2 views')
plt.title('Hourly Correlation') 

plt.savefig('wikipedia.png')
