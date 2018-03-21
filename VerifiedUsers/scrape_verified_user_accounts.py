import constants
import time
import csv
import tweepy


def get_verified_user_data(number_of_users_to_scrape, get_user_profile, get_tweets):
    get_user_ids(number_of_users_to_scrape, get_user_profile, get_tweets)


def get_user_ids(number_of_ids_to_get, get_user_profile=True, get_tweets=False):
    ids = []

    # csv file to save verified user ID's
    #
    verified_user_ids = open("VerifiedUserIDs.csv", "w")
    writer = csv.writer(verified_user_ids)

    for page in tweepy.Cursor(constants.api.followers_ids, screen_name="verified").pages():
        print(page)
        for id_number in page:
            writer.writerow([id_number])
        ids.extend(page)
        if len(ids) >= number_of_ids_to_get:
            print(str(number_of_ids_to_get) + " ids acquired")
            break
        time.sleep(60)
        print("Current number of ids " + str(len(ids)))
    # END
    if get_user_profile and get_tweets:
        get_user_profiles(ids, True)
    elif get_user_profile:
        get_user_profiles(ids)


def read_user_id_csv(file_name, get_profiles=False, get_tweets=False):
    user_ids = []
    with open(str(file_name), 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            user_ids.extend(row)
    print("Done Reading User ID's")

    if get_profiles:
        get_user_profiles(user_ids)

    if get_tweets:
        get_user_tweets(user_ids)


def get_user_profiles(ids, get_tweets=False):
    verified_screen_names = open("VerifiedUserData.csv", "w")
    user_data_writer = csv.writer(verified_screen_names)
    header = ["id", "username", "screen_name", "location", "url", "description", "followers", "following",
              "favorite_count", "tweet_count", "created_at", "time_zone", "geo_enabled", "language",
              "profile_image_url", "default_profile", "default_profile_image"]

    user_data_writer.writerow(header)

    # lookup users is limited to 100 per request so this has to be chopped up and sent 100 at a time
    #
    sliced_ids = [ids[x:x + 100] for x in range(0, len(ids), 100)]
    # print(sliced_ids)

    count = 0
    for id_slice in sliced_ids:
        print("On slice " + str(count) + " out of " + str(len(sliced_ids)))
        count += 1
        user_slice = constants.api.lookup_users(user_ids=id_slice)
        for user in user_slice:
            # Twitter User Model https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object
            #
            user_data = [user.id_str, user.name, user.screen_name, user.location,
                         user.url, user.description, user.followers_count, user.friends_count,
                         user.favourites_count, user.statuses_count, user.created_at, user.time_zone,
                         user.geo_enabled, user.lang, user.profile_image_url, user.default_profile,
                         user.default_profile_image]
            user_data_writer.writerow(user_data)

    print("Done downloading user profiles")

    if get_tweets:
        print("Fetching user tweets")
        get_user_tweets(ids)
    # END


def get_user_tweets(user_ids):
    # This is just the user_id and the text from their last 100 tweets
    #
    all_user_tweets = open("VerifiedUserTweets.csv", "w")

    # This is the information about each tweet
    #
    tweet_info = open("VerifiedUserTweetInfo.csv", "w")

    # This is a combination of the above information
    #
    tweets_and_info = open("VerifiedUserTweetsAndInfo.csv", "w")

    writer = csv.writer(all_user_tweets)
    writer2 = csv.writer(tweet_info)
    writer3 = csv.writer(tweets_and_info)

    header = ["UserID"]

    for i in range(1, 101):
        header.append("Tweet " + str(i) + " text")

    header2 = ["UserID", "Source", "Language", "Favorite Count", "Retweet count",
               "Favorite Count / Retweet Count", "Is Quote", "Is Reply"]

    header3 = ["UserID", "Tweet Text", "Source", "Language", "Favorite Count", "Retweet count",
               "Favorite Count / Retweet Count", "Is Quote", "Is Reply"]

    writer.writerow(header)
    writer2.writerow(header2)
    writer3.writerow(header3)

    count = 0
    for user_id in user_ids:
        try:
            print("On id " + str(count) + " out of " + str(len(user_ids)))
            print("Current id: " + str(user_id))
            count += 1
            user_tweets = constants.api.user_timeline(user_id=user_id, count=100)

            last_100_tweets = [user_id]

            # id first then all of the tweets
            #

            for tweet in user_tweets:
                last_100_tweets.append(tweet.text)

                if tweet.in_reply_to_status_id is not None:
                    is_reply = True
                else:
                    is_reply = False

                if tweet.retweet_count > 0:
                    ratio = tweet.favorite_count / float(tweet.retweet_count)
                else:
                    # Prevent divide by zero error
                    #
                    ratio = 0

                info = [user_id, tweet.source, tweet.lang, tweet.favorite_count, tweet.retweet_count,
                        ratio, tweet.is_quote_status, is_reply]
                writer2.writerow(info)

                # Write to tweets and info
                #
                more_info = [user_id, tweet.text, tweet.source, tweet.lang, tweet.favorite_count, tweet.retweet_count,
                             ratio, tweet.is_quote_status, is_reply]
                writer3.writerow(more_info)
            # END

            writer.writerow(last_100_tweets)

        except tweepy.TweepError:
            print("Failed to run command on user " + str(user_id) + " this user will be skipped")

    print("Done downloading user tweets")
    # END


