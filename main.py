from bs4 import BeautifulSoup as bs
import requests
import json
from pprint import pprint



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
    products = []
    for url in page_urls:
        req = requests.get(url).content
        product_divs = bs(req, 'html.parser').find_all('div', class_='caption info-inner')
        
        for div in product_divs:
            name = div.find('a').text.replace('\n', '').split()  # format product name, removeing \n and extra spaces
            price = div.find('span', class_='price').text.replace('AED ', '')
            products.append({' '.join(name):price}) # join name with spaces in dict before appending to product list
    
    return products


def convPrice(price):
    req = requests.get('https://api.exchangerate-api.com/v4/latest/AED').json()
    return str(float(price) * req['rates']['USD'])[:5]

