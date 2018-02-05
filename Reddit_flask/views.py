##########################################################################################################
#Functions for viewing html templates
##########################################################################################################
from flask import Flask, render_template, request, redirect, url_for
from Reddit_flask import app
from Reddit_flask.recommender import find_type,find_product,find_similar_product,skintype_recommend, popular_products
import pandas as pd, csv

reddit_users = pd.read_csv('/home/ubuntu/Insight/Reddit_flask/ABsubreddit_users.csv')
product_ids = [77,3,299,10,289,263]
products = pd.read_csv('/home/ubuntu/Insight/Reddit_flask/MakeupAlley_products_1.csv')

#process and display output
@app.route('/output')
def output():
    username = request.args.get('username')
    if username in reddit_users['username'].tolist():
        #Find user skintype and recommend products
        skintype = find_type(username)
        if not skintype:
            recommended1 = []
        else:
            skintype = skintype[0]
            if skintype.lower() == 'dehydrated':
                skintype = 'dry'
            recommended1 = skintype_recommend(skintype)
        #Find products and recommended products
        popular = popular_products(product_ids)
        searched_products = find_product(username)
        if not searched_products:
            recommended2 = []
            found_product = ''
        else:
            recommended2 = find_similar_product(searched_products[0])
            found_product = searched_products[0]
        return render_template("output.html", skintype=skintype, product=found_product, recommended1 = recommended1, recommended2=recommended2,popular=popular)
    else:
        return render_template("Home.html",error="Can't find this user! Try another username")


#display homepage
@app.route('/')
def input():
    return render_template("Home.html")

#display About product_images
@app.route('/Aboutme')
def about():
    return render_template("Aboutme.html")

#display How it works page
@app.route('/Howitworks')
def how():
    return render_template("Howitworks.html")

@app.route('/Home')
def home():
    return render_template("Home.html")
