import scrapingFunction as sf

# input the person page url
url_person = 'https://movie.douban.com/people/lingrui1995/'

# select the first page of 看过的电影
movieCollection = {} # the collected movie set
urlCollect = url_person + '/collect' # 看过的电影
nextPage = True

while nextPage != False:
    moviePage = sf.getPage(urlCollect)
    movieCollection = sf.getMovie(moviePage, movieCollection)
    nextPage = sf.checkNextPage(moviePage)
    urlCollect = 'https://movie.douban.com' + nextPage
    print('collect 1 page')