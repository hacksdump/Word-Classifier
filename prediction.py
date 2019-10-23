from utils.xml_tree_parse import get_map_from_xml
from config.paths import TEST_WORD_TAG_FILE, TEST_DIR
from utils.training import Training
import os

# Clean file before writing
open(TEST_WORD_TAG_FILE, 'w').close()

train_data = Training().train_data
prediction = {}

# Now open file in append mode to write all tags
with open(TEST_WORD_TAG_FILE, 'a') as write_word_tag:

    # Iterate through all files in Train-corpus directory
    for filename in os.listdir(TEST_DIR):
        path = os.path.join(TEST_DIR, filename)
        # Ignore directories... no recursive walking
        if not os.path.isfile(path):
            continue
        print("Parsing {}".format(filename))
        with open(path) as xml_file:
            word_tag = get_map_from_xml(xml_file)
            for word, tag in word_tag:
                print("{}_{}".format(word, tag), file=write_word_tag)
                prediction[word] = {
                    'actual': tag,
                }
                if word in train_data:
                    prediction[word]['predicted'] = train_data[word]
                else:
                    prediction[word]['predicted'] = "NA"
