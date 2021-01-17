"""Processes lines in the text files and extracts words and processes them"""

__license__ = "Rashed Karim"
__revision__ = " $Id: WordProcessor.py 1 2021-01-17 drkarim $ "

# Python libraries
from nltk.tokenize import word_tokenize
from nltk import sent_tokenize
from nltk.corpus import stopwords

# Custom libraries
from InterestingWords import Word, WordsList, WordInformation

class TextParser:
    """
        Text processing for word extraction and storing them with their associated sentences in memory
    """
    @classmethod
    def Text_2_Word(cls, text: str, word_list: WordsList, doc_name: str):
        """
        Processes any text containing any number of sentences
        by extracting words and their assoc. sentences

        :param text: the text of the line
        :return: list of words
        """
        sentences = sent_tokenize(text)

        for sentence in sentences:
            words = TextParser.setence_2_word(sentence)

            for word in words:
                word_list.insert_word(word, sentence, doc_name)

        return word_list

    @classmethod
    def setence_2_word(cls, sentence: str):
        """
        Extracts words from a line using whitespace and punctuations as delimiter

        :param sentence: must be a sentence without punctuation in the end
        :return: list of words
        """
        tokens = word_tokenize(sentence)
        tokens_lc = [t.lower() for t in tokens]  # lowercase
        tokens_lc_alpha = [t for t in tokens_lc if t.isalpha()]  # filter punctuation

        # remove stopwords
        stop_words = set(stopwords.words('english'))
        words = [w for w in tokens_lc_alpha if not w in stop_words]

        return words



text = """ Let me express my thanks to the historic slate of candidates who accompanied me on this journey, 
            and especially the one who traveled the farthest - a champion for working Americans and an inspiration to my daughters and to yours -- 
            Hillary Rodham Clinton. To President Clinton, who last night made the case for change as only he can make it; to Ted Kennedy, 
            who embodies the spirit of service; and to the next Vice President of the United States, 
            Joe Biden, I thank you. I am grateful to finish this journey with one of the finest statesmen of our time, 
            a man at ease with everyone from world leaders to the conductors on the Amtrak train he still takes home every night."""
wl = WordsList()

wl = TextParser.Text_2_Word(text, wl, "doc1")
word_h = wl.word_list[1].word_information_list[0].to_string(format="html", word="express")
print(word_h)
print(wl)