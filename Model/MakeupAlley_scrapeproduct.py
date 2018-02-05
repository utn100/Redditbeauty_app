import string
import time
import requests
import re
import pandas as pd
import numpy as np
import bs4
from bs4 import BeautifulSoup
import urllib.request


df = pd.DataFrame()
product_ids = []
product_names =[]
product_brands = []
product_types =[]
ingredients =[]
number_reviews = []
product_urls = []
image_urls = []



product_id = 0
for i in range(40,57):
    url = 'https://www.makeupalley.com/product/searching.asp/CategoryId=7/NumberOfReviews=100/SC=HOWMANY/SD=DESC/page=%d' %(i+1)
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')
    tds = soup.find_all('td',class_='no-align')


    for j in np.arange(1,len(tds),3):
        print(product_id+1)
        product_ids.append(product_id + 1)
        product_url = 'https://www.makeupalley.com'+tds[j].find_all('a')[1].get('href')
        product_urls.append(product_url)
        no_review = tds[j].find_all('span')[2].text.split()[0]
        if ',' in no_review:
            no_review = int(no_review.replace(',',''))
        else:
            no_review = int(no_review)
        number_reviews.append(no_review)
        product_names.append(tds[j].find_all('a')[1].text)
        product_types.append(tds[j].find_all('span')[0].text)
        product_brands.append(tds[j].find_all('span')[1].text)
        product_r = requests.get(product_url)
        product_soup = BeautifulSoup(product_r.text,'html.parser')

        if len(product_soup.find_all('div',class_='product-image product-detail-image'))>0:
            image_urls.append(product_soup.find_all('div',class_='product-image product-detail-image')[0].find_all('img')[0].get('src'))
        else:
            image_urls.append('NA')
        if len(product_soup.find_all('div',class_='product-ingredients'))>0:
            ingredients.append(product_soup.find_all('div',class_='product-ingredients')[0].find_all('span')[0].text)
        else:
            ingredients.append('NA')

df['product_id'] = product_ids
df['product_name'] = product_names
df['product_brand'] = product_brands
df['product_type'] = product_types
df['ingredients'] = ingredients
df['number_reviews'] = number_reviews
df['product_url'] = product_urls
df['image_url'] = image_urls

df.to_csv('MakeupAlley_products_3.csv')
