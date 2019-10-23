from utils.xml_tree_parse import get_map_from_xml
from config.paths import TEST_WORD_TAG_FILE, TEST_DIR, PREDICTION_FILE
from utils.training import Training
import os
import csv

train_data = Training().train_data
prediction = {}
UNKNOWN_TAG = "UNC"

with open(TEST_WORD_TAG_FILE, 'w+') as write_word_tag:
    with open(PREDICTION_FILE, 'w+', newline='') as prediction_csv_file:
        prediction_field_names = ["word", "actual", "predicted"]
        prediction_csv_writer = csv.DictWriter(
            prediction_csv_file, fieldnames=prediction_field_names)
        prediction_csv_writer.writeheader()
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
                        prediction[word]['predicted'] = UNKNOWN_TAG
                    prediction_csv_writer.writerow(
                        {
                            "word": word,
                            "actual": prediction[word]['actual'],
                            "predicted": prediction[word]['predicted']
                        }
                    )
