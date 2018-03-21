from BotAccounts import scrape_suspected_bot_accounts

bot_names = scrape_suspected_bot_accounts.get_bot_names()

# for name in bot_names:
#     print("On bot " + name)
#     followers = scrape_suspected_bot_accounts.get_bots_followers(name)

followers = scrape_suspected_bot_accounts.get_bots_followers(bot_names[-1])
