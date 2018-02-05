import pandas as pd
import numpy as np
import csv, string

import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from textblob import TextBlob
import regex
from nltk import bigrams
import operator
from collections import Counter

distance = np.loadtxt(open("/home/ubuntu/Reddit_flask/combined_dist.csv", "rb"), delimiter=",")
distance_df = pd.DataFrame(distance)
products = pd.read_csv('/home/ubuntu/Reddit_flask/MakeupAlley_products_1.csv')
brands = products['full_name']
skintypelist = ['dry','dehydrated','oily','acne','sensitive','combo','combination']
groupby_skintype = pd.read_csv('/home/ubuntu/Reddit_flask/groupby_skintype.csv')
reddit_users = pd.read_csv('/home/ubuntu/Reddit_flask/ABsubreddit_users.csv')


#Function to find products based on skin type
def skintype_recommend(skintype):
    mask = groupby_skintype[(groupby_skintype['skin_type'] == skintype)&(groupby_skintype['mean_rating']>4.2)&(groupby_skintype['product_type'] == 'Masks')].sort_values('count',ascending=False).head(3)
    moisturizer = groupby_skintype[(groupby_skintype['skin_type'] == skintype)&(groupby_skintype['mean_rating']>4.2)&(groupby_skintype['product_type'] == 'Moisturizers')].sort_values('count',ascending=False).head(3)
    cleanser = groupby_skintype[(groupby_skintype['skin_type'] == skintype)&(groupby_skintype['mean_rating']>4.2)&(groupby_skintype['product_type'] == 'Cleansers')].sort_values('count',ascending=False).head(3)
    masks = []
    moisturizers = []
    cleansers = []
    for i in range(0,mask.shape[0]):
        masks.append({'name':mask['full_name'].iloc[i],'size':5000,'url':mask['product_url'].iloc[i]})
        moisturizers.append({'name':moisturizer['full_name'].iloc[i],'size':5000,'url':moisturizer['product_url'].iloc[i]})
        cleansers.append({'name':cleanser['full_name'].iloc[i],'size':5000,'url':cleanser['product_url'].iloc[i]})

    recommended = [{"name":skintype,
             "size":20000,
             "children": [{"name": "Masks",
                          "size": 10000,
                          "children": masks},
                          {"name": "Moisturizers",
                          "size": 10000,
                          "children": moisturizers},
                          {"name": "Cleansers",
                          "size": 10000,
                          "children": cleansers}]
                          }]
    return recommended
#Function to find top 10 similar product to the given product
def find_similar_product(product_name):
    product_id = products[products['full_name']== product_name]['product_id'].iloc[0]
    top = 3
    top_product_id = distance_df[product_id].sort_values(ascending=True)[1:top+1].index + 1
    top_name = products[products['product_id'].isin(top_product_id)]['full_name']
    top_product_url = products[products['product_id'].isin(top_product_id)]['product_url']
    top_image_file = products[products['product_id'].isin(top_product_id)]['image_file']
    recommended = []
    for i in range(0,top):
        recommended.append({'name':top_name.iloc[i],
                            'image_file':top_image_file.iloc[i],
                            'url':top_product_url.iloc[i]})
    return recommended

#Function to find skin type for user
def find_type(username):
    reddit_user = reddit_users[reddit_users['username'] == username]
    flair = str(reddit_user['flair'].iloc[0])
    skintypes = [word for word in skintypelist if word in flair.lower()]
    if not skintypes:
        comment_list = reddit_users[reddit_users['username']== username]['comment']
        combined_comment = ''
        for i in range(0,len(comment_list)):
            combined_comment = combined_comment + comment_list.iloc[i]

        blob = TextBlob(combined_comment)
        I_sentences = []
        for sentence in blob.sentences:
            if 'I' in sentence or 'my' in sentence:
                I_sentences.append(sentence)

        punctuation = list(string.punctuation)
        letter = list(string.ascii_lowercase)
        stop = stopwords.words('english') + punctuation + ['&amp;','rt', 'via','the','i','we','0'] + letter

        count_bigram = Counter()
        for sentence in I_sentences:
            word = [term for term in sentence.split(' ') if term not in stop]
            bigram = bigrams(word)
            count_bigram.update(bigram)

        skin_associated=[]
        num_bigram = len(count_bigram)
        for term in count_bigram.most_common(num_bigram):
            if 'skin' in term[0][1]:
                skin_associated.append(term[0][0])
                skintypes = [word for word in skin_associated if word in skintypelist]


    return skintypes


#Function to find the products mentioned by user
def find_product(username):
    reddit_user = reddit_users[reddit_users['username'] == username]
    products = []
    comments = []

    for comment in reddit_user['comment']:
        for product in brands:
            #Use regular expression to fuzzy match the product name to the product database
            if regex.findall(r'(?b)(?:'+product.lower()+'){e<=2}',comment.lower()):
                products.append(product)
                comments.append(comment)

    searched_products = pd.DataFrame()
    searched_products['item'] = products
    searched_products['comment'] = comments
    sentiments = []
    for comment in searched_products['comment']:
        sentiments.append(TextBlob(str(comment)).sentiment.polarity)
    searched_products['sentiment'] = sentiments
    recommended_products = searched_products[searched_products['sentiment']>=0]['item'].unique()

    return  list(recommended_products)

def popular_products(product_ids):
    top_name = products[products['product_id'].isin(product_ids)]['full_name']
    top_product_url = products[products['product_id'].isin(product_ids)]['product_url']
    top_image_file = products[products['product_id'].isin(product_ids)]['image_file']
    recommended = []
    for i in range(0,len(product_ids)):
        recommended.append({'name':top_name.iloc[i],
                            'image_file':top_image_file.iloc[i],
                            'url':top_product_url.iloc[i]})
    return recommended
