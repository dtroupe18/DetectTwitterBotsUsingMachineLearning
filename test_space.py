import tweepy
import constants


def start_paging(number_of_users_to):
    page_count = 1
    for page in tweepy.Cursor(constants.api.followers_ids, screen_name="verified").pages(3):
        process_page(page, page_count)


def process_page(page, number):
    print("Page ", number, "has ", len(page), "items")


start_paging()