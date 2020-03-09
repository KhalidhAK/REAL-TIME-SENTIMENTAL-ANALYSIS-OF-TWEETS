import tweepy
import numpy as np
import pandas as pd
from textblob import TextBlob
import re
import sys
from django.shortcuts import render
from django.template import Context,Template
from django.shortcuts import redirect



# consumer key & secret
CONSUMER_KEY = "t2EGDozPRRXDoa2rYtQkXnWYw"
CONSUMER_SECRET = "L3EyOsXiM0I6SLePDWf9sjU1dNyVogjHgoDjx8Qmqdl6PCpPTO"

# access token
ACCESS_TOKEN = "3881605529-EmvIVAo28rkuMmmjPo70rJf2Y7aVXbg86Rh6Ts8"
ACCESS_TOKEN_SECRET = "GjcA5iXvPFnYsd0ElU5NhSFoLcryBYD37ELL8DsYdVm7E"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)



df = pd.DataFrame(columns = ['Tweets', 'User', 'User_statuses_count', 
                             'user_followers', 'User_location', 'User_verified',
                             'fav_count', 'rt_count', 'tweet_date'])
# Create your views here.

def getInput(request):
    print(request);
    if request.method == 'POST':
        print(request.POST.get("search"));
        return redirect('/result/'+ request.POST.get("search")+ '/');
    else:
        return render(request,'app/home.html');


def clean_tweet(tweet):
    #print('Clean');
    return ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', ' ', tweet).split())
	
	
def analyze_sentiment(tweet):
   # print('sentiment');
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'


def stream(p,n,nt,data, file_name):
    #print("Inside stream");
    i = 0
    group = [];
    single = [];
    for tweet in tweepy.Cursor(api.search, q=data, count=100, lang='en',tweet_mode='extended').items():

        print(i, end='\r')
        #print(tweet.full_text);
        #single.append(tweet.user.location);
        df.loc[i, 'Tweets'] = tweet.full_text

        df.loc[i, 'User'] = tweet.user.name

        df.loc[i, 'User_statuses_count'] = tweet.user.statuses_count

        df.loc[i, 'user_followers'] = tweet.user.followers_count

        df.loc[i, 'User_location'] = tweet.user.location

        df.loc[i, 'User_verified'] = tweet.user.verified

        df.loc[i, 'fav_count'] = tweet.favorite_count

        df.loc[i, 'rt_count'] = tweet.retweet_count

        df.loc[i, 'tweet_date'] = tweet.created_at

        #t['coordinates'] = status.user.screen_name

        clean = clean_tweet(tweet.full_text)
        sentiment =analyze_sentiment(clean);
        if sentiment=="Positive":
            p=p+1;
        elif sentiment=="Negative":
            n=n+1;
        else:
            nt=nt+1;
        single.append(clean);
        #df['clean_tweet'] = df['Tweets'].apply(lambda x: clean_tweet(x))
		
        #df['Sentiment'] = df['clean_tweet'].apply(lambda x: analyze_sentiment(x))
        
        i+=1

        if i == 100:
            print(p,n,nt)
            break;
        else:
            pass
        group.append(single);
        single = [];
   

       
		

def main(request,data): 
    p = 0
    n = 0
    nt = 0
    i = 0
    group = [];
    country = [];
    tweets = [];
    tweet_date = [];
    for tweet in tweepy.Cursor(api.search, q=data, count=100, lang='en',tweet_mode='extended').items():

        print(i, end='\r')
        #single.append(tweet.user.location);
        clean = clean_tweet(tweet.full_text)
        if tweet.user.verified:
            temp = [];
            temp.append(tweet.user.name)
            temp.append(tweet.full_text);
            temp.append(tweet.created_at);
            temp.append(tweet.user.location)
            tweets.append(temp);
        sentiment =analyze_sentiment(clean);
        if sentiment=="Positive":
            p=p+1;
        elif sentiment=="Negative":
            n=n+1;
        else:
            nt=nt+1;
        #single.append(clean);
        if tweet.user.geo_enabled:
            print(tweet.place);
            if tweet.place:
                print(tweet.place.country_code);
                country.append(tweet.place.country_code);

        i+=1
        if i == 500:
            country.append("IN");
            #country.append("US");
            print(country)
            print(p,n,nt)
            break;
        else:
            pass
        
        
    return render(request,'app/result.html',{'p':p,'n':n,'nt':nt,'data':data,'tweets':tweets,'tweet_date':tweet_date,'country':country});