from config.paths import WORD_TAG_FREQUENCY_FILE


def get_word_tag_map(preprocessed_file):
    word_tag__frequency = {}
    with open(preprocessed_file) as preprocessed_file:
        for line in preprocessed_file:
            line = line.replace("\n", "")
            word, tag = line.split('_')
            key = (word, tag)
            if key in word_tag__frequency:
                word_tag__frequency[key] += 1
            else:
                word_tag__frequency[key] = 1

    return word_tag__frequency


def read_word_tag_frequency_file():
    word_tag__frequency_map = {}
    with open(WORD_TAG_FREQUENCY_FILE) as word_tag__frequency:
        for line in word_tag__frequency:
            line = line.replace("\n", "")
            word_tag, frequency = line.split(' ')
            frequency = int(frequency)
            word, tag = word_tag.split('_')
            word_tag__frequency_map[(word, tag)] = frequency
    return word_tag__frequency_map
