# Graph the frequency of each tweet count bin
#
import pandas as pd
import math
import matplotlib.pyplot as plt
import nltk
import matplotlib
from collections import Counter


def load_csv_into_dataframe(filename):
    return pd.read_csv(filename, header=0, sep=",")


# bot_df = load_csv_into_dataframe("DataAnalysis/BotUserData/BotUserData.csv")
# out = pd.cut(bot_df['tweet_count'], bins=[0, 1000, 5000, 10000, 25000, 50000, 100000, 500000, math.inf], include_lowest=True)
# ax = out.value_counts(sort=False).plot.bar(rot=0, color="b", figsize=(15,10))
#
# for c in out.cat.categories:
#     print("c: ", c)
#     print("c_left ", c.left)
#     print("c_right ", c.right)
#
#
# ax.set_xticklabels([c.left + " to " + c.left for c in out.cat.categories])
# plt.show()
#
# top_N = 10
#
#
#
# stopwords = nltk.corpus.stopwords.words('english')
# # RegEx for stopwords
# RE_stopwords = r'\b(?:{})\b'.format('|'.join(stopwords))
# # replace '|'-->' ' and drop all stopwords
# words = (df.plot_keywords
#            .str.lower()
#            .replace([r'\|', RE_stopwords], [' ', ''], regex=True)
#            .str.cat(sep=' ')
#            .split()
# )
#
# # generate DF out of Counter
# rslt = pd.DataFrame(Counter(words).most_common(top_N),
#                     columns=['Word', 'Frequency']).set_index('Word')
# print(rslt)
#
# # plot
# rslt.plot.bar(rot=0, figsize=(16,10), width=0.8)


""" THIS WORKS  """
#
# df = pd.read_csv(r'DataAnalysis/BotUserData/BotUserData.csv', usecols=['description'])
# print(df.description.str.split(expand=True).stack().value_counts())
#

# These characters will appear as their own word if not removed. This results in the hashtag
# being the most common word. This characters are removed from the results
#
my_stop_words = [',', '’', '#', '.', '!', '@', '&', ':', '|', '(', ')', '\'s', ';', '-', 'n\'t', '%']

# Read in just the bot profile descriptions
#
# bot_description_df = pd.read_csv("DataAnalysis/BotUserData/BotUserData.csv", usecols=['description'])

bot_hashtag_counts = []
bot_at_mention_counts = []
bot_description_lengths = []

for row_index, row in bot_description_df.iterrows():

    hashtag_count = str(row['description']).count('#')
    at_mention_count = str(row['description']).count('@')

    if isinstance(row['description'], float):
        # Some descriptions are blank which Pandas converts to NaN
        # Here we assign any row with NaN in the description to have a length of -1
        #
        description_length = -1
    else:
        description_length = len(str(row['description']))

    if description_length is None:
        print("Broken...")
        description_length = 0

    bot_hashtag_counts.append(hashtag_count)
    bot_at_mention_counts.append(at_mention_count)
    bot_description_lengths.append(description_length)

bot_df['hashtag_count'] = bot_hashtag_counts
bot_df['at_mention_count'] = bot_at_mention_counts
bot_df['description_length'] = bot_description_lengths
bot_df.head()
