# mytwitterbot.py
# IAE 101, Fall 2020
# Project 04 - Building a Twitterbot
# Name:
# netid:
# Student ID:

import sys
import time
import simple_twit
import urllib, json
import random
import requests
import os
import wikipedia


def get_image(event):
    page = wikipedia.page(event, auto_suggest=False)
    images = page.images
    for image in images:
        if image[-3:] == "jpg":
            return image
    if (len(page.images) == 0):
        return None
    return page.images[0]

def get_event():
    dict = {"event":"1" , "url":"1", "year":""}
    u = urllib.request.urlopen("https://history.muffinlabs.com/date")
    response = u.read()
    data = json.loads(response)
    event = random.choice(data['data']["Events"])
    dict["year"] = event["year"]
    dict["event"] = event["text"]
    dict["url"] = event["links"][0]["link"].split("/")[-1]
    return dict

# used to download image from wikipedia because tweepy requires local files
# https://stackoverflow.com/questions/31748444/how-to-update-twitter-status-with-image-using-image-url-in-tweepy
def download_image(api,url):
    filename = 'temp.jpg'
    if (url == None):
        return 0
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)
        return 1
    else:
        print("Unable to download image")
        return 0



def main():
    # This call to simple_twit.create_api will create the api object that
    # Tweepy needs in order to make authenticated requests to Twitter's API.
    # Do not remove or change this function call.
    # Pass the variable "api" holding this Tweepy API object as the first
    # argument to simple_twit functions.
    api = simple_twit.create_api()
    simple_twit.version()

    # Project 04 Exercises

    # Exercise 1 - Get and print 10 tweets from your home timeline

    # Exercise 2 - Get and print 10 tweets from another user's timeline

    # Exercise 3 - Post 1 tweet to your timeline.

    # Exercise 4 - Post 1 media tweet to your timeline.


    # YOUR BOT CODE BEGINS HERE
    # mytweets = simple_twit.get_home_timeline(api,10)
    # print("-------------10 Tweets from my timeline-------------")
    # print()
    #
    #
    #
    #
    # for tweet in mytweets:
    #     print(tweet.full_text)
    # #
    # print()
    # elsetweets = simple_twit.get_user_timeline(api, "nice_tips_bot", 10)
    # print("-------------10 Tweets from @nice_tips_bot-------------")
    # print()
    # for tweet in elsetweets:
    #     print(tweet.full_text)


    print("-------------Posting a tweet-------------")
    while True:
        event = get_event()
        image_status = download_image(api, get_image(event["url"]))
        message = "Today in year {y}, {e}".format(y =event["year"], e=event["event"])
        print(message)
        if (image_status == 1):
            simple_twit.send_media_tweet(api, message, "temp.jpg")
            os.remove("temp.jpg")
        elif(image_status == 0):
            simple_twit.send_tweet(api, message)
        time.sleep(900)




# end def main()

if __name__ == "__main__":
       main()
