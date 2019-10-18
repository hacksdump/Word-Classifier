from utils.map_word_tag import get_word_tag_map
from config.paths import WORD_TAG_FILE, WORD_TAG_FREQUENCY_FILE

word_tag__frequency = get_word_tag_map(WORD_TAG_FILE)
with open(WORD_TAG_FREQUENCY_FILE, 'w+') as write_word_tag_frequency:
    for (word, tag) in word_tag__frequency:
        key = (word, tag)
        write_word_tag_frequency.write(
            "{}_{} {}\n".format(word, tag, word_tag__frequency[key]))
