from utils.simple_count import SimpleCount
import numpy as np
from utils.map_word_tag import get_word_tag_map
from config.paths import TEST_WORD_TAG_FILE, PREDICTION_FILE
import csv
import seaborn

stats = SimpleCount()
tag_list = stats.tags_descending
tag_count = len(tag_list)
confusion_matrix = np.zeros((tag_count, tag_count))

correct_count = 0
incorrect_count = 1

with open(PREDICTION_FILE) as prediction_file:
    csv_reader = csv.DictReader(prediction_file)
    for row in csv_reader:
        if row['actual'] == row['predicted']:
            correct_count += 1
        else:
            incorrect_count += 1
        actual_index = tag_list.index(row['actual'])
        predicted_index = tag_list.index(row['predicted'])
        confusion_matrix[actual_index][predicted_index] += 1

for i in range(tag_count):
    for j in range(tag_count):
        print(confusion_matrix[i][j], end=" ")
    print()

accuracy = correct_count / (correct_count + incorrect_count)
print("Accuracy: ", accuracy)
