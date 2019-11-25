# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

from collections import defaultdict
import os
import sys
from config.paths import TRAIN_DIR, TEST_DIR, PARSED_DIR, HMM_FILE
import pickle
import numpy
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

START_TAG = "^"
END_TAG = "."


def get_default_dict_float():
    return defaultdict(float)


hmm_file_path = os.path.join(PARSED_DIR, HMM_FILE)
if os.path.exists(hmm_file_path) and not (len(sys.argv) > 1 and sys.argv[1] == "--train"):
    with open(hmm_file_path, "rb") as hmm_file_read:
        training_data = pickle.load(hmm_file_read)
    transition = training_data["transition"]
    emission = training_data["emission"]
    print("Train data exists on disk. Moving on to testing...")

else:
    transition = defaultdict(get_default_dict_float)
    emission = defaultdict(get_default_dict_float)

    def push_to_transition(tag_list):
        for i in range(1, len(tag_list)):
            previous_tags = tag_list[i - 1].split("-")
            current_tags = tag_list[i].split("-")
            for previous_tag in previous_tags:
                for current_tag in current_tags:
                    transition[previous_tag][current_tag] += 1
                    transition[previous_tag]["TOTAL"] += 1

    for file in os.listdir(TRAIN_DIR):
        if ".xml" in file:
            with open(os.path.join(TRAIN_DIR, file)) as xml_file:
                tree = ET.parse(xml_file)
                root = tree.getroot()

                for sentence in root.iter('s'):
                    # This tag list may contain start tag, end_tag, simple tags and compound tags.
                    # Actual filling of transition values will be handled by another subroutine.
                    tag_list = [START_TAG]
                    for word_data in sentence.iter("w"):
                        word = word_data.text.strip().lower()
                        metadata = word_data.attrib
                        simple_or_compound_tag = metadata["c5"]
                        tag_list.append(simple_or_compound_tag)
                        for tag in simple_or_compound_tag.split("-"):
                            emission[tag][word] += 1
                            emission[tag]["TOTAL"] += 1

                    tag_list.append(END_TAG)
                    push_to_transition(tag_list)

    for origin in transition:
        for terminus in transition[origin]:
            if terminus != "TOTAL":
                transition[origin][terminus] /= transition[origin]["TOTAL"]

    for tag in emission:
        for word in emission[tag]:
            if word != "TOTAL":
                emission[tag][word] /= emission[tag]["TOTAL"]

    with open(hmm_file_path, "wb") as hmm_file_write:
        pickle.dump({
            "transition": transition,
            "emission": emission
        }, hmm_file_write)
    print("Training Complete.")


#########################################
############### TESTING #################
#########################################
print("Testing begins")
tag_count = len(transition)
empirical_tag_list = [tag for tag in transition.keys() if tag != START_TAG]
empirical_tag_list = sorted(
    empirical_tag_list, key=lambda x: emission[x]["TOTAL"], reverse=True)


def get_tag_index(tag):
    return empirical_tag_list.index(tag)


confusion_matrix = numpy.zeros((tag_count, tag_count))


def purify_sentence(sentence):
    allowed_chars = [chr(x) for x in range(97, 97 + 26)] + ["'", " "]
    purified_sentence = "".join([
        char for char in sentence.lower().strip() if char in allowed_chars])
    return purified_sentence


def bigram_viterbi(words):
    predicted_tag_sequence = [START_TAG]

    for word in words:
        pred = max(empirical_tag_list,
                   key=lambda tag: transition[predicted_tag_sequence[-1]][tag] * emission[tag][word])
        predicted_tag_sequence.append(pred)
    predicted_tag_sequence.pop(0)
    return predicted_tag_sequence


def matching_tag_count(sequence_one, sequence_two):
    if len(sequence_one) != len(sequence_two):
        return 0
    count = 0
    for i in range(len(sequence_one)):
        if sequence_one[i] in sequence_two[i] or sequence_two[i] in sequence_one[i]:
            count += 1
    return count


total_test_words = 0
correctly_predicted_test_words = 0
for file in os.listdir(TEST_DIR):
    if ".xml" in file:
        with open(os.path.join(TEST_DIR, file)) as xml_file:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            for sentence in root.iter('s'):
                words = []
                actual_tag_sequence = []
                for word_data in sentence.iter("w"):
                    total_test_words += 1
                    word = word_data.text.strip().lower()
                    words.append(word)
                    tag = word_data.attrib["c5"]
                    actual_tag_sequence.append(tag)
                predicted_tag_sequence = bigram_viterbi(words)
                correctly_predicted_test_words += matching_tag_count(
                    actual_tag_sequence, predicted_tag_sequence)

                # Filling the confusion matrix
                for i in range(len(actual_tag_sequence)):
                    compound_actual_tags = actual_tag_sequence[i]
                    for actual_tag in compound_actual_tags.split("-"):
                        actual_tag_index = get_tag_index(actual_tag)
                        predicted_tag_index = get_tag_index(
                            predicted_tag_sequence[i])
                        confusion_matrix[actual_tag_index][predicted_tag_index] += 1
    if "--quick-test" in sys.argv:
        break

prediction_accuracy = correctly_predicted_test_words / total_test_words
print("Prediction accuracy:", prediction_accuracy * 100, "%")

ax = sns.heatmap(confusion_matrix, xticklabels=empirical_tag_list,
                 yticklabels=empirical_tag_list)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plot_manager = plt.get_current_fig_manager()
plot_manager.full_screen_toggle()
plt.show()
