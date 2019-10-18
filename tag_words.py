#  -*- coding: utf-8 -*-

import os
from config.paths import TRAIN_DIR, WORD_TAG_FILE
from utils.xml_tree_parse import get_map_from_xml

# Clean file before writing
open(WORD_TAG_FILE, 'w').close()

# Now open file in append mode to write all tags
with open(WORD_TAG_FILE, 'a') as write_word_tag:

    # Iterate through all files in Train-corpus directory
    for filename in os.listdir(TRAIN_DIR):
        path = os.path.join(TRAIN_DIR, filename)
        # Ignore directories... no recursive walking
        if not os.path.isfile(path):
            continue
        print("Parsing {}".format(filename))
        with open(path) as xml_file:
            word_tag = get_map_from_xml(xml_file)
            for word, tag in word_tag:
                print("{}_{}".format(word, tag), file=write_word_tag)
