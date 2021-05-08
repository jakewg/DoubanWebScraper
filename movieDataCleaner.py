from datetime import datetime
from typing import Text
import pandas as pd
import re
df = pd.read_csv('movieInfo.csv')

# the data cleaning process begin >>>
# clean the type data
for i in range(len(df['type'])):
    data = df.loc[i, 'type']
    pattern = re.compile(r"[\u4e00-\u9fa5]{2,}") # regex pattern
    res = pattern.findall(data)
    ls = []
    for item in res:
        ls.append(item)
    df.loc[i, 'type'] = str(ls).replace('[', '').replace(']', '').replace("'", "")

# clean the director data
for i in range(len(df['director'])):
    data = df.loc[i, 'director']
    pattern = re.compile(r"[\u4e00-\u9fa5]{1,}·*[\u4e00-\u9fa5]*") # regex pattern of director
    res = pattern.findall(data)
    ls = []
    for item in res:
        ls.append(item)
    df.loc[i, 'director'] = str(ls).replace('[', '').replace(']', '').replace("'", "")

# clean the cast data
for i in range(len(df['cast'])):
    data = df.loc[i, 'cast']
    pattern = re.compile(r"[\u4e00-\u9fa5]{1,}·*[\u4e00-\u9fa5]*") 
    res = pattern.findall(data)
    ls = []
    for item in res:
        ls.append(item)
    df.loc[i, 'cast'] = str(ls).replace('[', '').replace(']', '').replace("'", "")

# clean the date data
for i in range(len(df['date'])):
    data = df.loc[i, 'date']
    pattern = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
    res = pattern.findall(data)
    text = str(res).replace('[', '').replace(']', '').replace("'", "")
    try:
        df.loc[i, 'date'] = datetime.strptime(text, '%Y-%m-%d').strftime('%m/%d/%Y')
    except ValueError:
        df.loc[i, 'date'] = None

# clean the movie name and only contain chinese name
for i in range(len(df['name'])):
    data = df.loc[i, 'name']
    pattern = re.compile(r"^[\u4e00-\u9fa5 0-9·]{1,}") 
    res = pattern.findall(data)
    df.loc[i, 'name'] = str(res).replace('[', '').replace(']', '').replace("'", "")

df = df.drop(columns=['url', 'imdb'])
# <<< the data cleaning process end

df.to_csv('data/cleanedData.csv', index=False) # save to data