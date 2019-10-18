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
            line = preprocessed_file.readline()
    return word_tag__frequency
