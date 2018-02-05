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
products = pd.read_csv('MakeupAlley_products.csv')
urls = products['product_url']
no_reviews = products['number_reviews']
product_ids = products['product_id']

ages=[]
skin_types =[]
skin_tones =[]
skin_temps = []
usernames = []
reviews = []
ids = []
ratings = []

for i in range(0,len(urls)):
    print(i)
    url = urls[i]
    product_id = int(product_ids[i])
    if no_reviews[i]%10==0:
        no_page = int(no_reviews[i]/10)
    else:
        no_page = int(no_reviews[i]/10) + 1

    for page in range(0,no_page):
        r = requests.get('/'.join(url.split('/')[0:6])+('/page=%d'%(page+1)))
        soup = BeautifulSoup(r.text,'html.parser')
        profiles = soup.find_all('div',class_='important')
        comments = soup.find_all('div','comment-content')
        user_names = soup.find_all('div','user-name')
        ratings_soup = soup.find_all('div',class_='lipies')
        for j in range(0,len(user_names)):
            ids.append(product_id)
            ages.append(profiles[j].find_all('p')[0].text.split(':')[1].strip(' :'))
            skin_types.append(profiles[j].find_all('p')[1].text.split(':')[1].strip(' :').split(',')[0])
            skin_tones.append(profiles[j].find_all('p')[1].text.split(':')[1].strip(' :').split(',')[1].strip(' '))
            skin_temps.append(profiles[j].find_all('p')[1].text.split(':')[1].strip(' :').split(',')[2].strip(' '))
            usernames.append(user_names[j].text.strip(' \t\t\t\t'))
            reviews.append(comments[j].text.strip(' \t\t\t'))
            ratings.append(int(ratings_soup[j].find('span').get('class')[0].split('-')[1]))


df['product_id'] = ids
df['user_id'] = usernames
df['age'] = ages
df['skin_type'] = skin_types
df['skin_tone'] = skin_tones
df['skin_temp'] = skin_temps
df['review'] = reviews
df['user_rating'] = ratings
df.to_csv('MakeupAlley_users.csv')
