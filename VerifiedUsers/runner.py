from VerifiedUsers import scrape_verified_user_accounts

header = ["id", "username", "screen_name", "location", "url", "description", "followers", "following",
          "favorite_count", "tweet_count", "average_tweets_per_day", "date_of_last_tweet", "account_age_in_days",
          "created_at", "time_zone", "geo_enabled", "language", "profile_image_url", "default_profile",
          "default_profile_image"]

scrape_verified_user_accounts.write_header_to_csv("LatestVerifiedUserData.csv", header)

scrape_verified_user_accounts.get_verified_users(10000)
