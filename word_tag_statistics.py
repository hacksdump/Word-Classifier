from utils.simple_count import SimpleCount
from config.paths import WORD_TAG_FREQUENCY_FILE

import matplotlib.pyplot as plt

word_tag_stats = SimpleCount(WORD_TAG_FREQUENCY_FILE)
top_ten_words = word_tag_stats.words_descending[:10]
top_ten_word_count = [word_tag_stats.word_count[word]
                      for word in top_ten_words]
print("Top 10 words: ", top_ten_words)
plt.pie(top_ten_word_count, labels=top_ten_words)
plt.show()

top_ten_tags = word_tag_stats.tags_descending[:10]
top_ten_tag_count = [word_tag_stats.tag_count[tag] for tag in top_ten_tags]
print("Top 10 tags: ", (word_tag_stats.tags_descending[:10]))
plt.pie(top_ten_tag_count, labels=top_ten_tags)
plt.show()
