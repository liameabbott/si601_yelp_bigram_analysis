#Yelp Bigram Analysis
An analysis of bigrams occurring in the user reviews of bars in the Yelp Dataset Challenge dataset

For this project, I analyzed Yelp user reviews of businesses categorized as bars. The goal was to count the most frequently used two-word phrases in both positive and negative reviews, and to compare the frequency with which these words were used in reviews with the frequency of their use in the English language, as measured by Google Books’ n-gram corpora.

The 'data_preprocess.py' script takes the two Yelp JSON datasets ('yelp_academic_dataset_business.json' and 'yelp_academic_dataset_review.json') as input and extracts the text of the positive (5-star) reviews of bars and the text of the negative (2 or fewer stars) reviews of bars. These reviews are written to the tab-delimited .txt files, 'pos_bigrams.txt' and 'neg_bigrams.txt'. The Yelp JSON dataset files are not included in this repository but are available for download from http://www.yelp.com/dataset_challenge. 

The 'bigram_analysis.py' script takes those text files as input and conducts the word count analysis that is the focus of this project. The script two more text files, 'pos_bgs_cts_probs.txt' and 'neg_bgs_cts_probs.txt', that contain every bigram found in the user reviews, the number of times that bigram occurred, and the probability of it occurring. 

The probabilities for ten selected, commonly-occurring bigrams from positive and negative reviews are compared to the probability of occurrence in the English language, as provided by the Google Books N-gram Viewer (https://books.google.com/ngrams). To extract this information from the Viewer, my analysis script imports and uses the nifty getngrams.py script written by Matt Nicklay, GitHub user econpy (https://www.github.com/econpy/google-ngrams). This code is based on code originally written by the Culturomics team at Harvard University. A description of the original Culturomics code can be found at http://www.culturomics.org/Resources/get-ngrams. 

I compare the review probabilities of the selected bigrams to the English language probabilities of those same bigrams by creating plots ('pos_probs_chart.pdf' and 'neg_probs_chart.pdf') of the log-ratio of these probabilities.

A more in-depth discussion of the project and code can be found in the 'bigram_project_report.pdf' file.
