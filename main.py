from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import pickle
from datetime import date, timedelta



def getLinks():
    req = requests.get('https://www.physiomart.ae/').content
    divs = bs(req, 'html.parser').find_all('div', class_=['parentMenu noSubMenu', 'parentMenu'])

    # append all links to list, skipping unused links and preventing duplicate links
    links = []
    unused_li = ['Home', 'Blog', 'Special Offers', 'New Arrivals']
    for div in divs:
        link = div.find('a')['href']
        if div.find('span').text in unused_li or link in links:
            pass
        else:
            links.append(link)

    return links


def getProductInfo(page_urls):
    products = {}
    for url in page_urls:
        req = requests.get(url).content
        product_divs = bs(req, 'html.parser').find_all('div', class_='caption info-inner')
        
        for div in product_divs:
            a_tag = div.find('a')
            link = a_tag['href']
            name = a_tag.text.replace('\n', '').split()  # format product name, removeing \n and extra spaces
            price = div.find('span', class_='price').text.replace('AED ', '').replace(',', '') # remove currency and comma in order to convert to float

            # join name with spaces before adding values to dict, convert price str to float for price comparison later
            products[' '.join(name)] = [float(price), link]
    
    return products


def readPickle(file):
    with open(file + '.pkl', 'rb') as pickle_file:
        return pickle.load(pickle_file)


def writePickle(data, file):
    with open(file + '.pkl', 'wb') as pickle_file:
        pickle.dump(data, pickle_file)


# get todays date, yesterdays date or 7 days from today
def getDate(prev=False, future=False):
    if prev:
        date_output = date.today() - timedelta(1)
    elif future:
        date_output = date.today() + timedelta(7)
    else:
        date_output = date.today()

    return str(date_output)