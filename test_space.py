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

my_stop_words = [',', '’', '#', '.', '!', '@', '&', ':', '|', '(', ')', '\'s', ';', '-', 'n\'t', '%']

df = pd.read_csv(r'DataAnalysis/BotUserData/BotUserData.csv', usecols=['description'])
top_N = 50

a = df['description'].str.lower().str.replace(r'#', '').str.cat(sep=' ')
words = nltk.tokenize.word_tokenize(a)
word_dist = nltk.FreqDist(words)

stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(my_stop_words)

print("Stop words: ", stopwords)
words_except_stop_dist = nltk.FreqDist(w for w in words if w not in stopwords)

# rslt = pd.DataFrame(word_dist.most_common(top_N), columns=['Word', 'Frequency'])
rslt = pd.DataFrame(words_except_stop_dist.most_common(top_N), columns=['Word', 'Frequency']).set_index('Word')
print(rslt)
