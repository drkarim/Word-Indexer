"""Processes lines in the text files and extracts words and processes them"""

__license__ = "Rashed Karim"
__revision__ = " $Id: WordProcessor.py 1 2021-01-17 drkarim $ "

from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np

# Custom libraries
import InterestingWords



class WordImportance:
    """
        Understands importance of words in a given corpus by calculating an importance score for each word
    """
    def __init__(self):
        self.word_importance_score = {}
        self.dataset = None

    def set_dataset(self, dataset):
        self.dataset = dataset

    def get_word_importance_score(self, word: str):

        if word in self.word_importance_score:
            return self.word_importance_score[word]
        else:
            return -1

    def compute_tf_idf(self):
        """
        Uses SkLearn's built-in Tf-Idf vectoriser to measure importance score for each word in the entire corpus
        Averages the word's tf-idf across all documents.
        Note, the averaging does not account for 0 scores for the word in a document,
        i.e. does not penalise the word for not occuring in a document

        :return: returns the td-idf scores of each word
        """
        tfIdfVectorizer = TfidfVectorizer(use_idf=True)
        tfidf_vec = tfIdfVectorizer.fit_transform(self.dataset)

        tfidf = tfidf_vec.todense()
        # Replacing TFIDF of words given 0 score (not in doc) with nan
        tfidf[tfidf == 0] = np.nan
        means = np.nanmean(tfidf, axis=0)
        means = dict(zip(tfIdfVectorizer.get_feature_names(), means.tolist()[0]))

        return means
