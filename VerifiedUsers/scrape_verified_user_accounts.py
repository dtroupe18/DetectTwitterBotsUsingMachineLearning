import constants
import csv
import datetime
import tweepy
import time
from requests.exceptions import Timeout, ConnectionError
from urllib3.exceptions import ReadTimeoutError, ProtocolError, SSLError


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


def days_between_dates(date_one, date_two):
    """
    :param date_one: datetime.datetime
    :param date_two: datetime.datetime
        https://docs.python.org/3/library/datetime.html#datetime-objects
    :return: Int - number of days between those two dates
    """
    d1 = datetime.date(date_one.year, date_one.month, date_one.day)
    d2 = datetime.date(date_two.year, date_two.month, date_two.day)
    delta = d2 - d1
    print("Days: ", delta.days)
    if abs((d2 - d1).days) > 0:
        return delta.days
    else:
        # Account could be 0 days old and cause a division by zero error
        #
        return 1


def get_daily_tweet_average(user):
    """
    :param user: user object from Twitter
        # https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object
    :return: Double - average tweets per day, date of last tweet, and account age in days
    """
    if 'status' in dir(user):
        status = user.status

        if status is None:
            # User as never tweeted so we ignore their account
            #
            print("Not status for ", user.name, " not a bot")
            return 0, 0, days_between_dates(user.created_at, datetime.datetime.now().date())
        else:
            print("{} {}".format("account created at:", user.created_at))
            print("{} {}".format("last status created at:", status.created_at))

            account_age_in_days = days_between_dates(user.created_at, status.created_at)
            average_tweets_per_day = user.statuses_count / account_age_in_days

            if average_tweets_per_day >= 25:
                print(user.name, " is likely to be a bot with ", average_tweets_per_day, " tweets per day")
                return average_tweets_per_day, status.created_at, account_age_in_days
            else:
                print(user.name, " is NOT likely to be a bot with ", average_tweets_per_day, " tweets per day")
                return average_tweets_per_day, status.created_at, account_age_in_days
    else:
        return 0, 0, days_between_dates(user.created_at, datetime.datetime.now().date())


def get_verified_users(number_of_users_to_scrape):
    """
    This function fetches the userId's and profiles for the
    :param number_of_users_to_scrape: int
    :return: creates a csv file where each row is a user profile
    """
    count = 0
    try:
        for page in tweepy.Cursor(constants.api.followers_ids, screen_name="verified").pages():
            print("length of page ", len(page))

            for id_number in page:
                if count < number_of_users_to_scrape:
                    print("Number of ids: ", count)
                try:
                    user = constants.api.get_user(id_number)
                    average_tweets_per_day, date_of_last_tweet, account_age_in_days = get_daily_tweet_average(user)

                    # check and see if that user if that user is like a bot or not
                    #
                    if average_tweets_per_day < 10:

                        data = [user.id_str, user.name, user.screen_name, user.location,
                                user.url, user.description, user.followers_count, user.friends_count,
                                user.favourites_count, user.statuses_count, average_tweets_per_day,
                                date_of_last_tweet, account_age_in_days, user.created_at, user.time_zone,
                                user.geo_enabled, user.lang, user.profile_image_url, user.default_profile,
                                user.default_profile_image]

                        add_row_to_csv("LatestVerifiedUserData.csv", data)
                        add_row_to_csv("LatestVerifiedUserIDs.csv", [user.id_str])
                        print("Added verified user: ", user.name)
                        count += 1
                    else:
                        print("User acts like a bot: ", user.name)

                except tweepy.TweepError as e:
                    print("Error encountered for ", id_number)
                    print("Error response", e.response)
                    print("\n")

                else:
                    print("number of ids: ", count)
                    break

            if count > number_of_users_to_scrape - 1:
                break

    except tweepy.TweepError as e:
        print("Error response", e.response)
        print("\n")

    except (Timeout, SSLError, ConnectionError, ReadTimeoutError, ProtocolError) as exc:
        print('2nd exception')
        time.sleep(150)

    print("Finished finding", number_of_users_to_scrape, "verified users who do not exhibit bot like behavior.")
    # END




