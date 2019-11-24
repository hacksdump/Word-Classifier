# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

from collections import defaultdict
import os
from config.paths import TRAIN_DIR

START_TAG = "^"
END_TAG = "."

transition = defaultdict(lambda: defaultdict(float))
emission = defaultdict(lambda: defaultdict(float))


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
        print("Parsing", file)
        with open(os.path.join(TRAIN_DIR, file)) as xml_file:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            for sentence in root.iter('s'):
                num = sentence.attrib["n"]
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


def purify_sentence(sentence):
    allowed_chars = [chr(x) for x in range(97, 97 + 26)] + ["'", " "]
    purified_sentence = "".join([
        char for char in sentence.lower().strip() if char in allowed_chars])
    return purified_sentence


def viterbi(sentence):
    sentence = purify_sentence(sentence)
    words = sentence.split(" ")
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

    predicted_tags = []
    for word in words:
        predicted_tags.append(
            max(dp_dict, key=lambda tag: dp_dict[tag][word])
        )
    print(predicted_tags)


viterbi("this virus affects the body")
