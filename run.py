#!./env/bin/python

################################
########### WEEK 1 #############
################################

# Problem statement: Bring the corpus into required format. (preprocessing)
# word1_tag
# word2_tag
import tag_words


################################
############ WEEK 2 ############
################################

# Problem statement: Create a dictionary having entry for unique word+tag combination with it's frequency
# count in the corpus.
import word_tag_frequency

################################
############ WEEK 3 ############
################################

# Problem statement: Report top 10 frequently used words and 10 frequently used tags. Provide your analysis of
# the word and tag distribution in the corpus.

# Word frequency Preprocessing
# Unique word map
import word_tag_statistics

################################
############ WEEK 4 ############
################################

# Problem statement: For each word, compute probabilities of word associations with tags. Program should be
# able to display probability of each word given the tag for the training corpus.
import training

################################
############ WEEK 5 ############
################################

# Problem statement: Predict the new tags for the words in the test corpus.
import prediction

################################
############ WEEK 6 ############
################################

# Generate confusion matrix for the word-tag pair.
import confusion
