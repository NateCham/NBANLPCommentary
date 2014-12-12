# NBA NLP - Final Project - CSC 582
# Data Scraping  - Inside Hoops
# Jacob Bustamante

import re
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup


# get_page
# Gets the raw binary data for the insidehoops webpage.
# If is_local is True (default), the local file is read,
#  if is_local is False, the page is fetched from the given URL.
def get_page(url="http://www.insidehoops.com/schedule.shtml", is_local=True):
    directory = "./webpages/insidehoops_schedule/NBA Schedule - InsideHoops.com.html"
    
    if is_local:
        raw = open(directory, 'rb').read()
    else:
        try:
            raw = urlopen(url, timeout=2).read()
        except:
            raise Exception("URL timed out:", url)
    
    return raw

