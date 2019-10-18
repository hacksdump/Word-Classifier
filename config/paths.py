import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Store folder names
TEST_DIR = os.path.join(BASE_DIR, 'Test-corpus')
TRAIN_DIR = os.path.join(BASE_DIR, 'Train-corpus')
PARSED_DIR = os.path.join(BASE_DIR, 'parsed')
WORD_TAG_FILE = os.path.join(PARSED_DIR, 'word_tag.txt')
