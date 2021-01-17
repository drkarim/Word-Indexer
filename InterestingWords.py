"""Data structures for storing interesting words and their relevant information"""

__license__ = "Rashed Karim"
__revision__ = " $Id: InterestingWords.py 1 2021-01-17 drkarim $ "
import ntpath
import os

class WordsList:
    """This class encapsulates a container for Words

        Words are a list of objects of :class:`Word` that in turn contain a list of :class:`WordInformation`"""

    def __init__(self):
        self.word_list = []

    def insert_word_obj(self, word_obj):
        """
        Insert a :class:`Word` object into the list

        :param word_obj:
        :return:
        """
        if not self.check_word_exists(word_obj):
            self.word_list.append(word_obj)

    def insert_word(self, word: str, sentence: str = "", document_name: str = ""):
        """
        Accepts a word string to insert as a :class:`Word` object into the container

        :param word: the word to be inserted as string
        :param sentence: a sentence as string this word occurs in, default leave blank
        :param document_name: the document name as string form for the sentence, default leave blank
        :return:
        """
        # turn the word and its information into a class objects
        word_obj = Word(word)
        word_information_obj = WordInformation(sentence, document_name, word)
        word_obj.insert_word_information(word_information_obj)

        # check if word exists to avoid duplication
        location = self.find_word(word)

        if location < 0:        # word not found
            self.word_list.append(word_obj)
        else:
            if location < len(self.word_list):
                self.word_list[location].insert_word_information(word_information_obj)
            else:
                return Exception('Location the word was found was out of bounds of the container')


    def find_word(self, word_str: str):
        """
        Looks for the word by doing a string in lowercase comparision and returns location of match

        :param word_str: the word being searched
        :return: The index of where the word was foumd, -1 if it was not found
        """
        index = 0
        word_str_lc = word_str.lower()
        for word in self.word_list:

            if word.get_word() == word_str_lc:
                return index

            index = index + 1

        return -1


    def to_string(self, format: str = "html"):
        """
        String representation of WordList

        :param format: format: By default uses html
        :return: returns string representation
        """
        content = ""
        if format == "html":

            content = """
            <html>
                <head>
                    <style>
                    table, th, td {
                      border: 1px solid black;
                    }
                    </style>
                </head>
                <body>
                    <h2>Word Index</h2>
            
            """

            table_header = """
                <table style="width:100%; border: 1px solid black;"> 
                    <tr><td>Word (Total Occurences)</td><td>Documents</td><td>Sentences containing the word</td></tr>
            """

            content = content + table_header
            for word in self.word_list:

                content = content + "<tr>"

                word_col = "<td>" + word.get_word() + "</td>"
                doc_col = "<td>" + word.get_word_documents() + "</td>"
                sentences_col = "<td>" + word.get_word_sentences() + "</td>"

                content = content + word_col + doc_col + sentences_col + "</tr>"

            content = content + "</table></body></html>"
        else:
            content = ""

        return content





class Word:
    """
    This class represents a Word
    A word can have a list of its occurrences. This information lists the sentences and documents the word occurs in.

    """
    def __init__(self, word_str: str):
        self.word_str = word_str.lower()
        self.word_information_list = []

    def get_word(self):
        return self.word_str

    def insert_word_information(self, word_information_obj):
        """
        Insert information about a word as a :class:`WordInformation`
        :param word_information_obj:

        """
        if not self.check_word_information_exists(word_information_obj):
            self.word_information_list.append(word_information_obj)

    # Is the exact same information about this word in the list already
    # NEED TO WRITE IMPLEMENTATION
    def check_word_information_exists(self, word_information_obj):
        return False

    def get_word_information(self):
        """
        Get information about the word, i.e. a list of all sentences and all documents it occurs in

        :return: returns a list of :class:`WordInformation` objects
        """
        return self.word_information_list


    def get_word_documents(self):
        """
        Documents this word occurs in
        :return: List of documents as a comma separated string
        """
        doc_list = []
        for inf in self.word_information_list:
            doc_list.append(inf.get_document_name())
        doc_set = set(doc_list)
        doc_list_str = ', '.join(doc_set)
        return doc_list_str

    def get_word_sentences(self):
        """
        The sentences in which the word occurs

        :return: A single string representation of all sentences
        """
        sentence_list = []
        for inf in self.word_information_list:
            sentence_list.append(inf.to_string(format="html"))

        sentence_list_str = '<br /><br />'.join(sentence_list)
        return sentence_list_str

'''
    Represents the information we store on words. 
    
    We store about each word, its:  
        - Sentence 
        - Name of document it is found in 
'''
class WordInformation:

    def __init__(self, sentence: str, document_name: str, word: str = None):
        self.sentence = sentence
        basename = WordInformation.get_filename_from_any_os_path(document_name)
        self.document_name = basename
        self.start_index = -1
        self.end_index = -1

        if word is not None:
            self.find_word_location(word)

    @classmethod
    def get_filename_from_any_os_path(cls, file_path):
        basename = ntpath.basename(file_path)
        return os.path.splitext(basename)[0]

    ''' 
        Set's and Get's 
    '''
    def set_document_name(self, document_name: str):
        # store basename only
        basename = WordInformation.get_filename_from_any_os_path(document_name)
        self.document_name = basename

    def set_sentence(self, sentence: str):
        self.sentence = sentence

    def set_sentence(self, word: str, sentence: str):
        self.find_word_location(word)
        self.sentence = sentence

    def find_word_location(self, word: str):
        sentence_lc = self.sentence.lower()  # lowercase sentence
        location = sentence_lc.find(word.lower())

        if location != -1:
            self.start_index = location

            if location + len(word) <= len(self.sentence):
                self.end_index = location + len(word)
            else:
                self.end_index = self.start_index + 1       # catch-all unexpected scenario
            return True
        else:
            return False


    def get_sentence(self):
        return self.sentence

    def get_document_name(self):
        return self.document_name

    def to_string(self):
        """
        Outputs a simple string representation
        :return: string representation of the words occurence
        """
        wordinfo_2_string = self.document_name + " CONTAINS " + self.sentence
        return wordinfo_2_string

    def to_string(self, format: str = "html", word: str = None):
        """
        Outputs a string representation by highlighting word provided in the sentence

        :param word: Provide the word to highlight in the sentence
        :param format: By default uses html <b></b> to mark string. Provide alternate marker character or string, e.g. asterix *
        :return: the string representing of the word's occurence
        """

        wordinfo_2_string = ""
        if format == "html":
            start_quote = " <b>"
            end_quote = "</b> "
        else:
            start_quote = format
            end_quote = format

        if self.start_index != -1:      # location of word not computed already
            start = self.start_index
            end = self.end_index

            word_quoted_in_sentence = self.sentence[:start-1] + start_quote + self.sentence[start:end] + end_quote + self.sentence[end+1:]

            # for debugging
            # wordinfo_2_string = self.document_name + " CONTAINS " + word_quoted_in_sentence
            wordinfo_2_string = word_quoted_in_sentence
        else:
            wordinfo_2_string = self.to_string()

        return wordinfo_2_string