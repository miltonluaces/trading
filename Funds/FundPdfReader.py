from os import path
import sys
sys.path.append(path.abspath('D:/source/repos/ProblemSolving/'))

# importing all the required modules
import PyPDF2

if __name__ == '__main__':

    
    # creating an object 
    file = open('example.pdf', 'rb')

    # creating a pdf reader object
    fileReader = PyPDF2.PdfFileReader(file)

