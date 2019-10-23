import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Store folder names
TEST_DIR = os.path.join(BASE_DIR, 'Test-corpus')
TRAIN_DIR = os.path.join(BASE_DIR, 'Train-corpus')
PARSED_DIR = os.path.join(BASE_DIR, 'parsed')
WORD_TAG_FILE = os.path.join(PARSED_DIR, 'preprocessed_train.txt')
WORD_TAG_FREQUENCY_FILE = os.path.join(PARSED_DIR, 'word_tag_frequency.txt')
TRAIN_DATA = os.path.join(PARSED_DIR, 'train_data.txt')
TEST_WORD_TAG_FILE = os.path.join(PARSED_DIR, 'preprocessed_test.txt')
PREDICTION_FILE = os.path.join(PARSED_DIR, 'prediction.csv')
