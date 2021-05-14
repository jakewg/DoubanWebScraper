import re
import requests
from bs4 import BeautifulSoup

def getPage(session, url):
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
            'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
            'Accept':'text/html,application/xhtml+xml,application/xml;'
            'q=0.9,image/webp,*/*;q=0.8'}
    req = session.get(url, headers = headers)
    bs = BeautifulSoup(req.text, 'html.parser')
    return bs
    
def getMovie(page, resDict):
# get all movie item in current page
    items = page.find_all('li', {'class': 'title'})
    for item in items:
        urlMovie = item.find('a')['href']
        titleMovie = item.find('em').contents[0]
        resDict[titleMovie] = urlMovie
    return resDict

def checkNextPage(page):
# see whether have the next page of this collection
    nextPage = page.find_all('span', {'class':'next'})
    for item in nextPage:
        try:
            return item.find('a')['href']
        except TypeError:
            return False

def getDate(page):
# get the first release data of the movie (based on website)
    date = page.find('span', {'property': 'v:initialReleaseDate'}).contents
    if date == []: # for movies without date
        date = ['None']
    else:
        pass
    return date

def getRating(page):
# get the movie rating
    try:
        rating = page.find('strong', {'class':'ll rating_num'}).contents
        return float(rating)
    except AttributeError: # the movie may be limited
        return None

def getType(page):
# get the movie type
    type = [] # could has different types
    for i in page.find_all('span', {'property': 'v:genre'}): 
        type.append(i.contents[0])
    return type

def getDirector(page):
# get the director of the movie
    director = [] # could has different director
    divInfo = page.find('div', {'id': 'info'})
    spans = divInfo.find_all('span')[0].find_all('a') # the first span is for directors
    for span in spans:
        director.append(span.contents[0])
    return director

def getCast(page):
# get the cast of the movie
    cast = [] # could has different director
    spans = page.find('span', {'class':'actor'}).find_all('a') # the first span is for directors
    for span in spans:
        cast.append(span.contents[0])
    return cast

def getImdb(page):
# get the imdb url of the movie
    for i in page.find_all('a'): # find all url
        try:
            text = i['href'] 
            url = re.search(r'.*imdb.com/title/.*', text) # find the url contain imdb
            if url == None:
                pass
            else:
                imdb = url.string
                break
        except KeyError:
            imdb = 'None'
    return imdb

def getCountry(page):
# get the producing country of the movie
    country = page.find('span', text = '制片国家/地区:').next_sibling
    return country

def getCollDate(page):
# get collection date <- cookies needed
    collectDate = page.find('span', {'class': 'collection_date'}).text
    return collectDate

def getStars(page):
# get stars number date <- cookies needed
    rateStar = page.find('div', {'class': 'j a_stars'}).find('input', \
        {'id':'n_rating'}).attrs['value']
    return int(rateStar)

def getRateText(page):
# get rating content date <- cookies needed
    text = page.find('div', {'class': 'j a_stars'}).find_all('span')[-2].text
    return text.strip()