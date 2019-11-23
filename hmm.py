# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

from collections import defaultdict

START_TAG = "^"
END_TAG = "."

transition = defaultdict(lambda: defaultdict(int))


def push_to_transition(tag_list):
    size_list = len(tag_list)
    if size_list == 2 and tag_list[0] == START_TAG and tag_list[-1] == END_TAG:
        return
    if size_list == 1 and tag_list[0] == END_TAG:
        return
    # It is assumed that the current tag, i.e. the first element in the list
    # is always a single tag like ^ or NN1 not a compound tag like NN1-VBZ.
    # This situation is ensured at the time this function is called.
    current_tag = tag_list[0]
    # Next can be a single tag or a conjunction of ambiguous tags like NN1-VBZ.
    # Thus whenever we see such tags, we need to branch there to accomodate multiple
    # such cases. A recursive tree if formed for many such cases in a single sentence.
    next_tags = tag_list[1]
    next_tags = next_tags.split("-")
    for next_tag in next_tags:
        transition[current_tag][next_tag] += 1
        transition[current_tag]["total"] += 1
        push_to_transition([next_tag] + tag_list[2:])


with open("./Train-corpus/A00.xml") as xml_file:
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for sentence in root.iter('s'):
        # This tag list may contain start tag, end_tag, simple tags and compound tags.
        # Actual filling of transition values will be handled by another subroutine.
        tag_list = [START_TAG, END_TAG]
        for word in sentence.iter("w"):
            metadata = word.attrib
            tag = metadata["c5"]
            tag_list.insert(1, tag)
        push_to_transition(tag_list)

print(transition)
