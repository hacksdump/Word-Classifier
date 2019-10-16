#!./env/bin/python
import os
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import sys

# Store folder names
TEST_DIR = './Test-corpus'
TRAIN_DIR = './Train-corpus'
PARSED_DIR = './parsed'
PARSED_SIMPLE = PARSED_DIR + '/word-tag'
PARSED_META = PARSED_DIR + '/word-metadata'

# Store word data in a map
# {
#   (word, tag)[tuple/pair] : count[int]
# }
word_map = {}

################################
########### WEEK 1 #############
################################

# Problem statement: Bring the corpus into required format. (preprocessing)
# word1_tag word2_tag

# Iterate through all files in Train-corpus directory
for filename in os.listdir(TRAIN_DIR):
    path = TRAIN_DIR + '/' + filename
    if not os.path.isfile(path):
        continue
    print("Parsing", filename)
    with open(path) as train_data:
        # Generate tree object from XML file
        tree = ET.parse(train_data)
        # Get root element of tree
        root = tree.getroot()
        generate_file_name = filename.split('.')[0] + '.txt'
        with open(PARSED_SIMPLE + '/' + generate_file_name, 'w') as write_parsed:
            # Scanning all 'w' tags in XML file
            for word_data in root.iter('w'):
                metadata = word_data.attrib
                word = word_data.text.strip().lower()
                tag = metadata['pos']
                write_parsed.write("{}_{}\n".format(word, tag))
                # Store word data in word map
                if (word, tag) in word_map:
                    word_map[(word, tag)] += 1
                else:
                    word_map[(word, tag)] = 1

################################
############ WEEK 2 ############
################################

# Problem statement: Create a dictionary having entry for unique word+tag combination with it's frequency
# count in the corpus.

with open(PARSED_META + '/' + 'final.txt', 'w') as write_parsed:
    for (word, tag) in word_map:
        print("{}_{} {}".format(
            word, tag, word_map[(word, tag)]), file=write_parsed)

################################
############ WEEK 3 ############
################################

# Problem statement: Report top 10 frequently used words and 10 frequently used tags. Provide your analysis of
# the word and tag distribution in the corpus.

# Word frequency Preprocessing
# Unique word map
uniq_word_count = {}
for (word, tag) in word_map:
    if word in uniq_word_count:
        uniq_word_count[word] += word_map[(word, tag)]
    else:
        uniq_word_count[word] = word_map[(word, tag)]

words_sorted_in_frequency_order = []
words_sorted_in_frequency_order = sorted(
    list(uniq_word_count), key=lambda item: uniq_word_count[item], reverse=True)

print("################ Words sorted in reverse frequency order ################")
top_ten_words = []
top_ten_word_count = []
for i in range(10):
    word = words_sorted_in_frequency_order[i]
    top_ten_words.append(word)
    top_ten_word_count.append(uniq_word_count[word])
    print(word, uniq_word_count[word])
# Plot pie chart
plt.pie(top_ten_word_count, labels=top_ten_words)
plt.show()

# Calculating tag frequency
tag_map = {}
for (word, tag) in word_map:
    if tag in tag_map:
        existing_tag_count = tag_map[tag]
    else:
        existing_tag_count = 0
    tag_map[tag] = existing_tag_count + word_map[(word, tag)]

tags_sorted_in_descending_order = []
tags_sorted_in_descending_order = sorted(
    list(tag_map), key=lambda item: tag_map[item], reverse=True)

print("################ Tags sorted in reverse frequency order ################")
top_ten_tags = []
top_ten_tag_count = []
for i in range(10):
    tag = tags_sorted_in_descending_order[i]
    top_ten_tags.append(tag)
    top_ten_tag_count.append(tag_map[tag])
    print("{} {}".format(tag, tag_map[tag]))

# Plot pie chart
plt.pie(top_ten_tag_count, labels=top_ten_tags)
plt.show()

################################
############ WEEK 4 ############
################################

# Problem statement: For each word, compute probabilities of word associations with tags. Program should be
# able to display probability of each word given the tag for the training corpus.

tag_word_map = {}
with open(PARSED_META + '/' + 'tag_bayes_freq.txt', 'w') as write_parsed:
    for (word, tag) in word_map:
        word_count_for_tag = word_map[(word, tag)]
        total_tag_count = tag_map[tag]
        probability = word_count_for_tag / total_tag_count
        write_parsed.write("{}_{} {}\n".format(word, tag, probability))

################################
############ WEEK 5 ############
################################

# Problem statement: Predict the new tags for the words in the test corpus.

# directory to store test data
test_map = {}

# Iterate through all files in Train-corpus directory
for filename in os.listdir(TEST_DIR):
    path = TEST_DIR + '/' + filename
    if not os.path.isfile(path):
        continue
    print("Parsing", filename)
    with open(path) as test_data:
        # Generate tree object from XML file
        tree = ET.parse(test_data)
        # Get root element of tree
        root = tree.getroot()
        # generate_file_name = filename.split('.')[0] + '.txt'
        with open(PARSED_SIMPLE + '/' + generate_file_name, 'w') as write_parsed:
            # Scanning all 'w' tags in XML file
            for word_data in root.iter('w'):
                metadata = word_data.attrib
                word = word_data.text.strip().lower()
                tag = metadata['pos']
                write_parsed.write("{}_{}\n".format(word, tag))
                # Store word data in test map
                if (word, tag) in test_map:
                    test_map[(word, tag)] += 1
                else:
                    test_map[(word, tag)] = 1

train_word_vs_tag = {}

for (word, tag) in word_map:
    if not word in train_word_vs_tag:
        train_word_vs_tag[word] = {}
    train_word_vs_tag[word][tag] = word_map[(word, tag)]

with open(PARSED_DIR + '/test_predictions.txt', 'w') as prediction_write:
    for (word, tag) in test_map:
        if word in train_word_vs_tag:
            predicted_tag = max(
                train_word_vs_tag[word].keys(), key=lambda item: train_word_vs_tag[word][item])
        else:
            predicted_tag = "NA"
        predictionIsCorrect = predicted_tag == tag
        prediction_write.write(word + "_" + predicted_tag +
                               [" *" + tag, ""][predictionIsCorrect] + "\n")
