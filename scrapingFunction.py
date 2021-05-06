import requests
from bs4 import BeautifulSoup

def getPage(url):
    session = requests.Session()
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