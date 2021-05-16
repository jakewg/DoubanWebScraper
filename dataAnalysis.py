#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

df = pd.read_csv('data/cleanedData.csv')
# drop the items without names since no name can not provide any relevant information
df = df.drop(df[df['name'].isna()].index).reset_index(drop=True)
#%%
# plot in the time series of movie release time with the count of movies
df['date'] = pd.to_datetime(df['date'])  # change the data time which we can separate month / year
df = df.sort_values(['date'])
for i in range(len(df['date'])):
    df.loc[i, 'month'] = df.loc[i, 'date'].month
    df.loc[i, 'year'] = df.loc[i, 'date'].year
    text = str(df.loc[i, 'date'].year) + '-' + str(df.loc[i, 'date'].month)
    df.loc[i, 'yearMonth'] = datetime.strptime(text, '%Y-%m').strftime('%Y/%m')
df['yearMonth'] = pd.to_datetime(df['yearMonth'])

fig, ax = plt.subplots(figsize=(15,7))
# use rolling().mean() for Moving-Average model
ax = df.groupby(['yearMonth']).size().rolling(12, center=True).mean().rolling(2, center=True).mean()
ax.plot()
plt.show()
# %%
