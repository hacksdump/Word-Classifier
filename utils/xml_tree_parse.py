#  -*- coding: utf-8 -*-


import xml.etree.ElementTree as ET


def get_map_from_xml(xml_file):
    word_tag = []
    file_should_be_closed = False
    if isinstance(xml_file, str):
        xml_file = open(xml_file, 'r')
        file_should_be_closed = True

    # Generate tree object from XML file
    tree = ET.parse(xml_file)

    # If file is created in this module, it should be closed here
    # Else it should be properly closed by the calling module.
    if file_should_be_closed:
        xml_file.close()

    # Get root element of tree
    root = tree.getroot()
    # Scanning all 'w' tags in XML file
    for word_data in root.iter('w'):
        metadata = word_data.attrib
        word = word_data.text.strip().lower()
        tags = metadata['c5'].split('/')
        for tag in tags:
            # Store word and tag in array
            word_tag.append((word, tag))

    return word_tag
