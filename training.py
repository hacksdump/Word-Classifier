from utils.training import Training
from config.paths import TRAIN_DATA

prediction = Training()
with open(TRAIN_DATA, 'w') as write_train_data:
    for word in prediction.train_data:
        write_train_data.write("{} {}\n".format(
            word, prediction.train_data[word]))
