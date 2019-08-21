#!./env/bin/python
import os
import xml.etree.ElementTree as ET

TRAIN_DIR = './Train-corpus'
PARSED_DIR = './parsed'
PARSED_SIMPLE = PARSED_DIR + '/word-tag'
PARSED_META = PARSED_DIR + '/word-metadata'
for filename in os.listdir(TRAIN_DIR):
    print("Parsing", filename)
    with open(TRAIN_DIR + '/' + filename) as train_data:
        word_map = {}
        tree = ET.parse(train_data)
        root = tree.getroot()
        generate_file_name = filename.split('.')[0] + '.txt'
        with open(PARSED_SIMPLE + '/' + generate_file_name, 'w') as write_parsed:
            for word_data in root.iter('w'):
                metadata = word_data.attrib
                word = metadata['hw']
                tag = metadata['pos']
                write_parsed.write("{}_{}\n".format(word, tag))
                if word in word_map:
                    word_map[word]['count'] += 1
                else:
                    word_map[word] = {
                        'tag': tag,
                        'count': 1
                    }

        with open(PARSED_META + '/' + generate_file_name, 'w') as write_parsed:
            for word in sorted(word_map):
                print(word, word_map[word], file=write_parsed)
