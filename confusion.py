from utils.simple_count import SimpleCount
import numpy as np
from utils.map_word_tag import get_word_tag_map
from config.paths import TEST_WORD_TAG_FILE, PREDICTION_FILE
import csv
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

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


ax = sns.heatmap(confusion_matrix, xticklabels=tag_list, yticklabels=tag_list)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plot_manager = plt.get_current_fig_manager()
plot_manager.full_screen_toggle()
plt.show()

accuracy = correct_count / (correct_count + incorrect_count)
print("Accuracy: ", accuracy)
