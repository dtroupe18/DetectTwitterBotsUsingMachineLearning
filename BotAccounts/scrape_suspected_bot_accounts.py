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
from datetime import date
import csv
import tweepy


def read_csv(file_name):
    """
    :param file_name: string "fileName.csv"
    :return: list of csv data
    """
    data = []
    with open(str(file_name), 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            data.extend(row)

    print("Finished reading ", file_name)
    return data


def write_header_to_csv(file_name, header):
    """
    :param file_name: string "fileName.csv"
    :param header: list of csv data for the first row
    :return:
    """
    csv_file = open(file_name, "w")
    writer = csv.writer(csv_file)
    writer.writerow(header)


def add_row_to_csv(file_name, row):
    """
    :param file_name: string "fileName.csv"
    :param row: row of data to add to csv
    :return:
    """
    with open(str(file_name), 'a') as csv_file:
        writer = csv.writer(csv_file)
        if type(row) is list:
            writer.writerow(row)
        else:
            writer.writerow([row])
        csv_file.close()


def get_original_bot_names():
    """
    Reads the csv of bot user names and returns a list
    :return: list of user names
    """
    return read_csv("HandPickedBotList.csv")


def get_bot_names_from_bot_user_data():
    data_column = []
    with open("BotUserData.csv", 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            # get the username column (i.e the second col)
            #
            username = row[1]
            print("username: ", username)
            data_column.append(username)

    csv_file.close()
    # pop the first element because it's the column header
    #
    data_column.pop(0)
    return data_column

    # data_frame = pd.read_csv("BotUserData.csv")
    # username_column = data_frame['username']
    # return username_column


def get_scraped_bot_names():
    return read_csv("BotNamesWhoseFollowersWereScraped.csv")


def get_remaining_bot_names():
    original_names = get_original_bot_names()
    scraped_names = set(get_scraped_bot_names())

    # return all the names that are in original names, but not in scraped_names
    #
    return [x for x in original_names if x not in scraped_names]


def get_bots_followers(bot_name, debug=False):
    """
    :param debug: Bool whether to print debug values or not
    :param bot_name: string Twitter user name
    :return:
    """
    # Add this user name to our csv so we know not to scrape this account again
    #
    add_row_to_csv("BotNamesWhoseFollowersWereScraped.csv", bot_name)
    try:
        for user in tweepy.Cursor(constants.api.followers, screen_name=bot_name).items(200):
            if debug:
                print("{} {}".format("userId:", user.id))
                print("{} {}".format("follower count:", user.followers_count))
                print("{} {}".format("friends count:", user.friends_count))
                print("{} {}".format("account created at:", user.created_at))
                print("{} {}".format("status count:", user.statuses_count))

            if is_likely_a_bot(user):
                # This user is likely to be a bot so add them to the list
                #
                data = [user.id_str, user.name, user.screen_name, user.location,
                        user.url, user.description, user.followers_count, user.friends_count,
                        user.favourites_count, user.statuses_count, user.created_at, user.time_zone,
                        user.geo_enabled, user.lang, user.profile_image_url, user.default_profile,
                        user.default_profile_image]

                add_row_to_csv("BotUserData.csv", data)
                add_row_to_csv("BotUserIDs.csv", [user.id_str])
            print("\n")

    except tweepy.TweepError as e:
        print("Error encountered for ", bot_name)
        print("Error response", e.response)
        print("\n")


def days_between_dates(date_one, date_two):
    """
    :param date_one: datetime.datetime
    :param date_two: datetime.datetime
        https://docs.python.org/3/library/datetime.html#datetime-objects
    :return: Int - number of days between those two dates
    """
    d1 = date(date_one.year, date_one.month, date_one.day)
    d2 = date(date_two.year, date_two.month, date_two.day)
    delta = d2 - d1
    print("Days: ", delta.days)
    if abs((d2 - d1).days) > 0:
        return  delta.days
    else:
        # Account could be 0 days old and cause a division by zero error
        #
        return 1


def is_likely_a_bot(user):
    """
    :param user: user object from Twitter
        # https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object
    :return: Bool True is a bot, false otherwise
    """
    if 'status' in dir(user):
        status = user.status

        if status is None:
            # User as never tweeted so we ignore their account
            #
            print("Not status for ", user.name, " not a bot")
            return False
        else:
            print("{} {}".format("account created at:", user.created_at))
            print("{} {}".format("last status created at:", status.created_at))

            account_age_in_days = days_between_dates(user.created_at, status.created_at)
            average_tweets_per_day = user.statuses_count / account_age_in_days

            if average_tweets_per_day >= 25:
                print(user.name, " is likely to be a bot with ", average_tweets_per_day, " tweets per day")
                return True
            else:
                print(user.name, " is NOT likely to be a bot with ", average_tweets_per_day, " tweets per day")
                return False
