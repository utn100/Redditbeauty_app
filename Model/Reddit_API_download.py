import praw
import pandas as pd
import csv
import string

#Input reddit API access info (regiter on )
reddit = praw.Reddit(client_id='t1U14fLy65aQAQ',
                     client_secret='iFB3KRyqYsfmEbKtcdQG5K19INU',
                     user_agent='Subchannel_API')

#Download a subreddit
subreddit = reddit.subreddit('AsianBeauty')

#Download oneyear of reddit data
hot_AB = subreddit.submissions(1483228800,1514764800)
comments = []
thread_id = []
thread_ids =[]
linkflair=[]
user_comments =[]
flairs = []
usernames=[]
thread_titles=[]
parents = []
collapsed=[]
i = 0
for thread in hot_AB:
    if (not thread.stickied) and thread.link_flair_text in ['Discussion','Hauls','Review']:
        thread_titles.append(thread.title)
        counter = i+1
        thread_id.append(i+1)
        linkflair.append(thread.link_flair_text)
        thread.comments.replace_more(limit=None)
        i = i+1
        for comment in thread.comments.list():
            thread_ids.append(counter)
            usernames.append(comment.author)
            flairs.append(comment.author_flair_text)
            user_comments.append(comment.body)

ABsubreddit_posts = pd.DataFrame()
ABsubreddit_posts['thread_id'] = thread_id
ABsubreddit_posts['thread_title'] = thread_titles
ABsubreddit_posts['link_flair_label'] = linkflair


ABsubreddit_comments = pd.DataFrame()
ABsubreddit_comments['thread_id'] = thread_ids
ABsubreddit_comments['username'] = usernames
ABsubreddit_comments['comment'] = user_comments
ABsubreddit_comments['flair'] = flairs

ABsubreddit_posts.to_csv('ABsubreddit_posts.csv')
ABsubreddit_comments.to_csv('ABsubreddit_users.csv')
