from config.paths import WORD_TAG_FREQUENCY_FILE


class SimpleCount:
    def __calculate_frequency(self):
        with open(self.word_tag_frequency_file) as word_tag__frequency:
            for line in word_tag__frequency:
                line = line.replace("\n", "")
                word_tag, frequency = line.split(' ')
                frequency = int(frequency)
                word, tag = word_tag.split('_')
                if word in self.word_count:
                    self.word_count[word] += frequency
                else:
                    self.word_count[word] = frequency
                if tag in self.tag_count:
                    self.tag_count[tag] += frequency
                else:
                    self.tag_count[tag] = frequency

    def __sort_descending(self):
        self.words_descending = sorted(
            list(self.word_count), key=lambda item: self.word_count[item], reverse=True)

        self.tags_descending = sorted(
            list(self.tag_count), key=lambda item: self.tag_count[item], reverse=True)

    def __init__(self, word_tag_frequency_file=WORD_TAG_FREQUENCY_FILE):
        self.word_tag_frequency_file = word_tag_frequency_file
        self.word_count = {}
        self.tag_count = {}
        self.words_descending = None
        self.tags_descending = None
        self.__calculate_frequency()
        self.__sort_descending()
