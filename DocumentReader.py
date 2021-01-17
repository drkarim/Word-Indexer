"""High-level Text Document Reader"""

__license__ = "Rashed Karim"
__revision__ = " $Id: DocumentReader.py 1 2021-01-17 drkarim $ "
import os
import argparse

# custom libraries
from InterestingWords import Word, WordsList, WordInformation, TextParser
from WordProcessor import WordImportance
'''
    Class represents text file reader   

'''
class DocumentReader:


    def __init__(self):
        self.data_folder_path = './data/'
        self.word_list = WordsList()
        self.full_dataset = []
        self.word_importance = None

    '''
        Sets and Gets 
    '''
    def SetDataFolderPath(self, pathname):
        self.data_folder_path = pathname

    # Read text file line-by-line
    def ReadDocumentFile(self, filename):

        all_lines = ''
        all_lines_list = []
        # read all lines within a file into one single line
        with open(filename, 'r') as file_object:
            lines = file_object.readlines()
            for line in lines:
                all_lines = all_lines + " " + line
                TextParser.text_2_word(line, self.word_list, filename)
                all_lines_list.append(line.lower())

        self.full_dataset.append(''.join(all_lines_list))

    def GetWordImportance(self):
        wi = WordImportance()
        wi.set_dataset(self.full_dataset)
        self.word_importance = wi.compute_tf_idf()
        self.word_list.insert_word_importance_scores(self.word_importance)

    def ReadDataFolder(self):
        """
        Process every text files file in the specified folder path specified in :py:data:`self.data_folder_path`

        """
        file_list = os.listdir(self.data_folder_path)
        for file_name in file_list:
            file_path = self.data_folder_path  + file_name

            if file_path.endswith('.txt'):          # only .txt files
                self.ReadDocumentFile(file_path)

    def WriteOutToHTML(self, filename, sort_order=None):
        """
        Writes the Word index to an HTML file
        :param filename: Specify filename of the HTML

        """
        self.word_list.sort_word_list(sort_order)

        html = self.word_list.to_string(format="html")

        # Write HTML String to file.html
        with open(filename, "w") as file:
            file.write(html)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", help="The path to the data files", required=True)
    parser.add_argument("--output", "-o", help="The path to write the output file", required=False)
    parser.add_argument("--sortorder", "-s", help="The sorting order, iaf, fai or f", required=False)

    args = parser.parse_args()
    doc_reader = DocumentReader()

    doc_reader.SetDataFolderPath(args.input)
    doc_reader.ReadDataFolder()
    doc_reader.GetWordImportance()

    if args.output is not None:
        doc_reader.WriteOutToHTML(args.output, args.sortorder)
