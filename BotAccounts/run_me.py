from BotAccounts import scrape_suspected_bot_accounts

# bot_names = scrape_suspected_bot_accounts.get_original_bot_names()

bot_names = scrape_suspected_bot_accounts.get_bot_names_from_bot_user_data()

header = ["id", "username", "screen_name", "location", "url", "description", "followers", "following",
          "favorite_count", "tweet_count", "average_tweets_per_day", "date_of_last_tweet", "account_age_in_days",
          "created_at", "time_zone", "geo_enabled", "language", "profile_image_url", "default_profile",
          "default_profile_image"]

scrape_suspected_bot_accounts.write_header_to_csv("FullBotUserData.csv", header)


for name in bot_names:
    print("On bot " + name)
    scrape_suspected_bot_accounts.get_bot_profile(name)
    # scrape_suspected_bot_accounts.get_bots_followers(name)

