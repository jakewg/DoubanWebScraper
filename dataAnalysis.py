#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
df = pd.read_csv('data/cleanedData.csv')
# drop the items without names since no name can not provide any relevant information
df = df.drop(df[df['name'].isna()].index).reset_index(drop=True)
#%%
# plot in the time series with the count of movies
df['date'] = pd.to_datetime(df['date'])  # change the data time which we can separate month / year
for i in range(len(df['date'])):
    df.loc[i, 'month'] = df.loc[i, 'date'].month
    df.loc[i, 'year'] = df.loc[i, 'date'].year
    df.loc[i, 'yearMonth'] = str(df.loc[i, 'date'].year) + '-' + str(df.loc[i, 'date'].month)

count = df["yearMonth"].value_counts().sort_index()
#%%
fig, ax = plt.subplots()
ax.plot(count.index, count.values)
# format the ticks
plt.xticks(np.arange(0, len(count), 10), rotation=30, ha='right')
plt.show()

