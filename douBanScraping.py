import scrapingFunction as sf
import time
import csv
import pandas as pd
import pickle
import requests

# input the person page url
url_person = 'https://movie.douban.com/people/1402913'
cookiesDict = pickle.load(open("cookies.pkl", "rb"))
s = requests.Session()
for cookie in cookiesDict:
    s.cookies.set(cookie['name'], cookie['value'])

# select the first page of 看过的电影
movieCollection = {} # the collected movie set
urlCollect = url_person + '/collect' # 看过的电影
nextPage = True

# run the scraper while the nextpage tag exists in webpage
pageNum = 0
while nextPage != False:
    moviePage = sf.getPage(s, urlCollect)
    movieCollection = sf.getMovie(moviePage, movieCollection)
    nextPage = sf.checkNextPage(moviePage)
    if nextPage != False:
        urlCollect = 'https://movie.douban.com' + nextPage
    else:
        print('No more page could be scraped')
        break
    pageNum += 1
    print(f'collect {pageNum} page')
    time.sleep(6)

# save the movie name and page url to csv
with open('data/movieCollection.csv', 'w') as csv_file:  
    writer = csv.writer(csv_file)
    writer.writerow(['name', 'url'])
    for key, value in movieCollection.items():
       writer.writerow([key, value])

# set movies' variable and read all moviess url
movieInfo = pd.DataFrame(columns=['name', 'url', 'date', 'rate', 'type',\
    'director', 'cast', 'country', 'imdb'])
itemNum = 0
dfMovie = pd.read_csv('data/movieCollection.csv')
# a loop to collect all relevant information of movies
for i in range(len(dfMovie['name'])):
    item = {} # collect one movie once in this dictionary
    item['name'] = dfMovie.iloc[i, 0]
    item['url'] = dfMovie.iloc[i, 1]
    page = sf.getPage(s, item['url'])
    if page.title.contents[0] == '页面不存在': # the page has been 404
        item['type'] = 404
        itemNum += 1
        print(f'No.{itemNum} --- {dfMovie.iloc[i, 0]} has been 404')
    else:
        item['date'] = sf.getDate(page)[0]
        item['rate'] = sf.getRating(page)[0]
        item['type'] = sf.getType(page)
        item['director'] = sf.getDirector(page)
        item['cast'] = sf.getCast(page)
        item['country'] = sf.getCountry(page)
        item['imdb'] = sf.getImdb(page)
        item['collectDate'] = sf.getCollDate(page)
        item['stars'] = sf.getStars(page)
        item['rateText'] = sf.getRateText(page)
        movieInfo = movieInfo.append(item, ignore_index=True)
        time.sleep(6)
        itemNum += 1
        print(f'collected {itemNum} movies')
# save the movie infomation
movieInfo.to_csv('data/movieInfo.csv', index=False)