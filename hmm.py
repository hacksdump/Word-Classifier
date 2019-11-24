# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

from collections import defaultdict
import os
import sys
from config.paths import TRAIN_DIR, TEST_DIR, PARSED_DIR, HMM_FILE
import pickle

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


def purify_sentence(sentence):
    allowed_chars = [chr(x) for x in range(97, 97 + 26)] + ["'", " "]
    purified_sentence = "".join([
        char for char in sentence.lower().strip() if char in allowed_chars])
    return purified_sentence


def viterbi(words):
    empirical_tag_list = [tag for tag in transition.keys() if tag != START_TAG]
    dp_dict = defaultdict(lambda: defaultdict(float))
    for i in range(len(words)):
        for tag in empirical_tag_list:
            if i == 0:
                dp_dict[tag][words[0]] = (
                    transition[START_TAG][tag] * emission[tag][words[0]])
            else:
                dp_dict[tag][words[i]] = max(
                    [
                        (
                            # Value from previous column
                            dp_dict[prev_tag][words[i-1]] *
                            # Transition value
                            transition[prev_tag][tag] *
                            # Emission value
                            emission[tag][words[i]]
                        )
                        for prev_tag in empirical_tag_list
                    ]
                )

    predicted_tag_sequence = []
    for word in words:
        predicted_tag_sequence.append(
            max(dp_dict, key=lambda tag: dp_dict[tag][word])
        )
    return predicted_tag_sequence


def are_tag_sequences_similar(sequence_one, sequence_two):
    if len(sequence_one) != len(sequence_two):
        return False
    for i in range(len(sequence_one)):
        if not sequence_one[i] in sequence_two[i] or not sequence_two[i] in sequence_one[i]:
            return False
    return True


total_test_sentences = 0
correctly_predicted_test_sentences = 0
for file in os.listdir(TEST_DIR):
    if ".xml" in file:
        with open(os.path.join(TEST_DIR, file)) as xml_file:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            for sentence in root.iter('s'):
                total_test_sentences += 1
                words = []
                actual_tag_sequence = []
                for word_data in sentence.iter("w"):
                    word = word_data.text.strip().lower()
                    words.append(word)
                    tag = word_data.attrib["c5"]
                    actual_tag_sequence.append(tag)
                predicted_tag_sequence = viterbi(words)
                if are_tag_sequences_similar(actual_tag_sequence, predicted_tag_sequence):
                    correctly_predicted_test_sentences += 1

prediction_accuracy = correctly_predicted_test_sentences / total_test_sentences
print("Prediction accuracy:", prediction_accuracy)
