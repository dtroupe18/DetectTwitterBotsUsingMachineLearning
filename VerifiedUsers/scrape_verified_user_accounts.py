import constants
import csv
from datetime import date
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
    # print("Days: ", delta.days)
    if abs((d2 - d1).days) > 0:
        return delta.days
    else:
        # Account could be 0 days old and cause a division by zero error
        #
        return 1


def get_verified_accounts(number_of_accounts, debug=False):
    """
    :param number_of_accounts: int
    :param debug: Bool whether or not to include print statements
    :return:
    """
    try:
        for user in tweepy.Cursor(constants.api.followers, screen_name="verified").items(200):
            if debug:
                print("{} {}".format("userId:", user.id))
                print("{} {}".format("follower count:", user.followers_count))
                print("{} {}".format("friends count:", user.friends_count))
                print("{} {}".format("account created at:", user.created_at))
                print("{} {}".format("status count:", user.statuses_count))

            if not exhibits_bot_like_behavior(user):
                # This account does not exhibit bot like behavior so we add them to the list
                #
                data = [user.id_str, user.name, user.screen_name, user.location,
                        user.url, user.description, user.followers_count, user.friends_count,
                        user.favourites_count, user.statuses_count, user.created_at, user.time_zone,
                        user.geo_enabled, user.lang, user.profile_image_url, user.default_profile,
                        user.default_profile_image]

                add_row_to_csv("VerifiedUserData.csv", data)
                add_row_to_csv("VerifiedUserIDs.csv", [user.id_str])
            print("\n")

    except tweepy.TweepError as e:
        print("Error encountered!")
        print("Error response", e.response)
        print("\n")


def exhibits_bot_like_behavior(user):
    """
    :param user: user object from Twitter
        # https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object
    :return: True if account has bot like behavior, false otherwise
        # here we consider an average of 25 or more tweets per day to be bot like behavior
    """
    if 'status' in dir(user):
        status = user.status

        if status is None:
            # User as never tweeted so we ignore their account
            #
            # print("Not status for ", user.name, " not adding them to verified users")
            return False
        else:
            # print("{} {}".format("account created at:", user.created_at))
            # print("{} {}".format("last status created at:", status.created_at))

            account_age_in_days = days_between_dates(user.created_at, status.created_at)
            average_tweets_per_day = user.statuses_count / account_age_in_days

            if average_tweets_per_day >= 25:
                print(user.name, " exhibits bot like behavior with ", average_tweets_per_day, " tweets per day")
                return True
            else:
                print(user.name, " does NOT exhibit bot like behavior with ", average_tweets_per_day, " tweets per day")
                return False


def get_verified_users(number_of_users_to_scrape):
    """
    This function fetches the userId's and profiles for the
    :param number_of_users_to_scrape: int
    :return: creates a csv file where each row is a user profile
    """
    count = 0

    for page in tweepy.Cursor(constants.api.followers_ids, screen_name="verified").pages(1):
        print("length of page ", len(page))

        for id_number in page:
            if count < number_of_users_to_scrape:
                print("Number of ids: ", count)
                # check and see if that user if that user is like a bot or not
                #
                user = constants.api.get_user(id_number)

                if exhibits_bot_like_behavior(user):
                    print("User acts like a bot: ", user.name)
                else:
                    print("User does not act like a bot: ", user.name)
                    count += 1
                    data = [user.id_str, user.name, user.screen_name, user.location,
                            user.url, user.description, user.followers_count, user.friends_count,
                            user.favourites_count, user.statuses_count, user.created_at, user.time_zone,
                            user.geo_enabled, user.lang, user.profile_image_url, user.default_profile,
                            user.default_profile_image]

                    add_row_to_csv("VerifiedUserData.csv", data)
                    add_row_to_csv("VerifiedUserIDs.csv", id_number)
            else:
                print("number of ids: ", count)
                break

        if count > number_of_users_to_scrape - 1:
            break

    print("Finished finding", number_of_users_to_scrape, "verified users who do not exhibit bot like behavior.")
    # END




