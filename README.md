# Redditbeauty_app

1/Motivation
During 3 weeks at Insight, I built RedditBeauty, a personalized recommender of skincare products for redditors who subscribed to the AsianBeauty subreddit.
These are the people who follow the Asian skincare routine that contains many steps (14-16). However at the rate of posts and comments produced, it creates confusion for these users of where to look for and pick their products.
2/Algorithms
I scraped 500 products in three categories (masks, moisturizers, cleansers) from MakeupAlley website, this included ~60K users (with skin type info) and >130K reviews.
I also pulled one year of data from the AsianBeauty subreddit.
From my MakeupAlley database, I built a hybrid recommender of: Cluster-based Smoothing Collaborative Filtering and Latent Semantic Analysis. 
The cluster-based smoothing approach helps alleviate the sparsity problem of my user-product matrix, while Latent Sematic Anlysis gave a better clustering of products in their categories.
This hybrid approach improved significantly over the traditional collaborative filtering.

Check out my app at: http://redditbeauty.club/
