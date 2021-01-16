import os
import argparse

'''
    Class represents text file reader   

'''
class DocumentReader:


    def __init__(self):
        self.data_folder_path = './data/'

    '''
        Sets and Gets 
    '''
    def SetDataFolderPath(self, pathname):
        self.data_folder_path = pathname


    # Read text file line-by-line
    def ReadDocumentFile(self, filename):

        with open(filename, 'r') as file_object:
            line = file_object.readline()
            print(line)

    # Iterate through only .txt files in a folder
    def ReadDataFolder(self):

        file_list = os.listdir(self.data_folder_path)
        for file_name in file_list:
            file_path = self.data_folder_path  + file_name

            if file_path.endswith('.txt'):          # only .txt files
                self.ReadDocumentFile(file_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", help="The path to the data files", required=False)
    parser.add_argument("--output", "-o", help="The path to write the output file", required=False)

    args = parser.parse_args()
    doc_reader = DocumentReader()

    doc_reader.SetDataFolderPath(args.input)
    doc_reader.ReadDataFolder()
