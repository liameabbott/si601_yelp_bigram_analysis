# -*- coding: utf-8 -*-
# !/usr/bin/python


import re
from itertools import groupby
from getngrams import runQuery as rq
import csv
import math
import numpy as np
import matplotlib.pyplot as plt


def bigram_counter(reviews):
    """Function takes as input a list whose elements are the text of individual
       business reviews and returns a list of lists, where each sub-list
       contains a bigram and the number of times that bigram was used in the
       reviews. The master list is sorted by the number of times each bigram
       was used, in descending order."""

    word_pattern = re.compile(r"\b[\w]+\b")

    # Create list of all bigrams in the list of reviews.
    bigram_list = []
    for review in reviews:
        words = word_pattern.findall(review)
        for i in range(len(words)-1):
            bigram = words[i].lower() + ' ' + words[i+1].lower()
            bigram_list.append(bigram)

    # Sort the bigram list alphabetically.
    sorted_bigram_list = sorted(bigram_list)

    # Using itertools groupby() function, count occurences of each bigram in
    # the sorted bigram list created above.
    bigram_counts_list = []
    for key, group in groupby(sorted_bigram_list, lambda x: x):
        bigram_count = 0
        for bigram in group:
            bigram_count = bigram_count + 1
        bigram_counts_list.append([key, bigram_count])

    bigram_counts_list_sorted = sorted(bigram_counts_list,
                                       key=lambda x: -x[1])

    # Return the sorted list of bigrams and their respective counts.
    return bigram_counts_list_sorted


# Open the .txt files containg the positive reviews.
with open('pos_reviews.txt', 'rU') as f:
    pos_reviews = f.readlines()

# Open the .txt files containg the negative reviews.
with open('neg_reviews.txt', 'rU') as f:
    neg_reviews = f.readlines()

# Create sorted lists of positive and negative bigrams and their counts.
pos_bgs_cts = bigram_counter(pos_reviews)
neg_bgs_cts = bigram_counter(neg_reviews)

# Count the total number of positive bigrams (not unqiue).
n_pos_bgs = 0.0
for i in range(len(pos_bgs_cts)):
    n_pos_bgs += float(pos_bgs_cts[i][1])

# Count the total number of negative bigrams (not unique).
n_neg_bgs = 0.0
for i in range(len(neg_bgs_cts)):
    n_neg_bgs += float(neg_bgs_cts[i][1])

# Calculate the probabilities of all positive bigrams by calculating the total
# number of occurrences of each bigram divided by the total number of bigrams
# in all positive reviews. Do the same for negative bigrams.
pos_bg_probs = [float(bg[1])/n_pos_bgs for bg in pos_bgs_cts]
neg_bg_probs = [float(bg[1])/n_neg_bgs for bg in neg_bgs_cts]

# Create list of lists where each sub-list contains a bigram, the number of
# occurrences of that bigram in positive reviews, and the probability of
# occurrence for that bigram. Sorted by most commonly occurring.
pos_bgs_cts_probs = []
for i in range(len(pos_bgs_cts)):
    bg = pos_bgs_cts[i][0]
    ct = pos_bgs_cts[i][1]
    prob = pos_bg_probs[i]
    pos_bgs_cts_probs.append([bg, ct, prob])

# Create list of lists where each sub-list contains a bigram, the number of
# occurrences of that bigram in negative reviews, and the probability of
# occurrence for that bigram. Sorted by most commonly occurring.
neg_bgs_cts_probs = []
for i in range(len(neg_bgs_cts)):
    bg = neg_bgs_cts[i][0]
    ct = neg_bgs_cts[i][1]
    prob = neg_bg_probs[i]
    neg_bgs_cts_probs.append([bg, ct, prob])

# Create a tab-delimited .txt file with list of bigrams, counts, probabilities
# found in positive reviews, sorted by most frequently occuring.
with open('pos_bgs_cts_probs.txt', 'wb') as f:
    for line in pos_bgs_cts_probs:
        f.write(line[0] + '\t' + str(line[1]) + '\t' + str(line[2]) + '\n')

# Create a tab-delimited .txt file with list of bigrams, counts, probabilities
# found in negative reviews, sorted by most frequently occuring.1
with open('neg_bgs_cts_probs.txt', 'wb') as f:
    for line in neg_bgs_cts_probs:
        f.write(line[0] + '\t' + str(line[1]) + '\t' + str(line[2]) + '\n')

# Set parameters for call to runQuery method in getngrams.py script
params = """ --startYear=2007 --endYear=2008 --corpus=eng_us_2012 --smoothing=3
             --caseInsensitive --noprint"""

# Set positive bigram and negative bigram queries to send to runQuery method in
# getngrams.py script.
pos_queries = ['the best', 'the food', 'the bar', 'i love', 'my favorite',
               'the service', 'the menu', 'happy hour', 'the staff',
               'great place']

neg_queries = ['the food', 'the bar', 'the service', 'no one', 'the manager',
               'the waitress', 'the bartender', 'my husband', 'it took',
               'the drinks']

# Call runQuery method on positive bigrams and negative bigrams.
pos_res = rq(', '.join(pos_queries) + params)
neg_res = rq(', '.join(neg_queries) + params)

# Open .csv files created by runQuery method and extract words and probability
# information for positive and negative bigrams.
param_file_handle = '-eng_us_2012-2007-2008-3-caseInsensitive.csv'
pos_file_handle = '_'.join(pos_queries).replace(' ', '')
neg_file_handle = '_'.join(neg_queries).replace(' ', '')

pos_filename = pos_file_handle + param_file_handle
neg_filename = neg_file_handle + param_file_handle

with open(pos_filename, 'rU') as f:
    l = [line for line in csv.reader(f, delimiter='\t')]
    pos_words = l[0][0]
    pos_probs = l[1][0]

with open(neg_filename, 'rU') as f:
    l = [line for line in csv.reader(f, delimiter='\t')]
    neg_words = l[0][0]
    neg_probs = l[1][0]

pos_eng_words = [word for word in pos_words.split(',')[1:]]
pos_eng_probs = [float(num) for num in pos_probs.split(',')[1:]]

neg_eng_words = [word for word in neg_words.split(',')[1:]]
neg_eng_probs = [float(num) for num in neg_probs.split(',')[1:]]

# Extract positive review probability of selected bigrams.
pos_rev_probs = []
for i in range(len(pos_bgs_cts_probs)):
    for word in pos_eng_words:
        if word == pos_bgs_cts_probs[i][0]:
            pos_rev_probs.append(pos_bgs_cts_probs[i][2])

# Extract negative review probability of selected bigrams.
neg_rev_probs = []
for i in range(len(neg_bgs_cts_probs)):
    for word in neg_eng_words:
        if word == pos_bgs_cts_probs[i][0]:
            neg_rev_probs.append(neg_bgs_cts_probs[i][2])

# Take the log of the ratio of positive review probability to English
# language probability for selected positive bigrams.
pos_log_ratios = [math.log(pos_rev_probs[i]/pos_eng_probs[i])
                  for i in range(len(pos_rev_probs))]

# Take the log of the ratio of negative review probability to English
# language probability for selected negative bigrams.
neg_log_ratios = [math.log(neg_rev_probs[i]/neg_eng_probs[i])
                  for i in range(len(neg_rev_probs))]

# Create and save bar plots of log-probabilities for positive and negative
# bigrams.
n_groups = 10
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.4

plt.figure()
pos_labels = [word.replace(' ', '\n') for word in pos_eng_words]
pos_bar = plt.bar(index, pos_log_ratios, bar_width, alpha=opacity,
                  color='r')
pos_line = plt.axhline(y=1.0, color='k', lw=2)
plt.title('Log of Prob(Pos Rev)/Prob(Eng Lang)')
plt.xticks(index+(bar_width/2), pos_labels)
plt.tight_layout()
plt.savefig('pos_probs_chart.pdf', bbox_inches='tight')

plt.figure()
neg_labels = [word.replace(' ', '\n') for word in neg_eng_words]
neg_bar = plt.bar(index, neg_log_ratios, bar_width, alpha=opacity,
                  color='b')
beg_line = plt.axhline(y=1.0, color='k', lw=2)
plt.title('Log of Prob(Neg Rev)/Prob(Eng Lang)')
plt.xticks(index+(bar_width/2), neg_labels)
plt.tight_layout()
plt.savefig('neg_probs_chart.pdf', bbox_inches='tight')
