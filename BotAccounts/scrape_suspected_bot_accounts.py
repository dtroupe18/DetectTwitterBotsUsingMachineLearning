# I looked over https://twitter.com/probabot_/lists/probably-bots/members and selected
# 50 accounts that I though were certainly bots. Some of these accounts are still active
# some of them are not.
#
# In order to expand the training set beyond 50 accounts this file will look at the followers
# of those 50 accounts. I will use one basic heuristic to determine if the account it a bot,
# the average number of tweets per day. If an account is averaging more than 25 tweets per day
# it will be flagged as a bot and added to our data.
#
# The number 25 was picked based on the research of two Berkley students
# https://medium.com/@robhat/an-analysis-of-propaganda-bots-on-twitter-7b7ec57256ae
#
# To get a broader sample of bots I will try to get approximately 100 bots from each
# account or ~ 5,000 total accounts.
#
# Using https://botcheck.me/ it appears that many of the bots I've selected are not flagged
# by the website the Berkley researchers created.
#

import constants
import time
import csv
import tweepy


def read_csv(file_name):
    data = []
    with open(str(file_name), 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            data.extend(row)

    print("Finished reading csv file.")
    return data


def get_bot_names():
    return read_csv("HandPickedBotList.csv")


def get_bots_followers(bot_name):
    followers = []

    for user in tweepy.Cursor(constants.api.followers, screen_name=bot_name).items(200):
        # print(user)
        print("{} {}".format("userId:", user.id))
        print("{} {}".format("follower count:", user.followers_count))
        print("{} {}".format("friends count:", user.friends_count))
        print("{} {}".format("created at:", user.created_at))

        if 'status' in dir(user):
            status = user.status

            if status is None:
                pass
            else:
                print("{} and {}".format("status created at:", status.created_at))

        followers.append(user.id)
        print("\n")

    print("Number of followers: " + str(len(followers)))
    return followers






