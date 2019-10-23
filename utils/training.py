from utils.map_word_tag import read_word_tag_frequency_file
from config.paths import WORD_TAG_FREQUENCY_FILE


class Training:
    def __generate_word_tag_mapping(self):
        intermediate_word_tag_map = {}
        word_tag__frequency = read_word_tag_frequency_file()
        for (word, tag) in word_tag__frequency:
            if not word in intermediate_word_tag_map:
                intermediate_word_tag_map[word] = {}
            if not tag in intermediate_word_tag_map[word]:
                intermediate_word_tag_map[word][tag] = 0
            intermediate_word_tag_map[word][tag] = word_tag__frequency[(
                word, tag)]
        for word in intermediate_word_tag_map:
            self.train_data[word] = max(
                intermediate_word_tag_map[word].keys(), key=lambda item: intermediate_word_tag_map[word][item])

    def __init__(self):
        self.train_data = {}
        self.__generate_word_tag_mapping()
