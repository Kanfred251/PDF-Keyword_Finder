import sys
import PyPDF2
import re
import nltk
import pandas as pd
import os
import fitz
import pdfplumber


# Writing the application to be run from this script

# Declaring my Constants
# Directory Path
path = r'C:\Users\Kanayo Anagbogu\Documents\NDA'

# Create list of absolute path names of files in directory and change working directory to NDA folder
os.chdir(path)
dir_list = os.listdir(path)
directory = []
for i in range(0,len(dir_list)-1):
    directory.append(os.path.abspath(dir_list[i]))

# Create Dataframe of the key words and the line they're found
df = pd.DataFrame(columns=['Filename', 'Keyword', 'Line'])

# Function to Strip Out "new line" data: Reduces "Extra data" that complicates further processing
def read_list_pages(list_pages):
    texts = []
    for word in list_pages:
        text = word.strip('\n')
        texts.append(text)
    return texts
# Function to tokenize the data (Separating each page by sentence)
def to_sent(page_list):
    sent_list = []
    for page in range(len(page_list)):
        sent_token = nltk.sent_tokenize(page_list[page])
        sent_list.append(sent_token)
    return sent_list

# Function to find and list out the keyword containing sentences
def find_sent_with_word(keyword, corpus):
    keyline = []
    for line in corpus:
        # line = line.lower()
        for key in keyword:
            result = re.search(r"(^|[^a-z])" + key + r"([^a-z]|$)", line)
            if result != None:
                keypair = (key, line)
                keyline.append(keypair)
                break
            else:
                pass
    return (keyline)

# Create an empty list to host the desired variables found from the documents
d = []

# Create a counter for the loop function to run on the documents
sum = 0

# The actual loop running on the individual docs
while sum < len(directory):
    # Assign the File
    file_name = directory[sum]

    #PYPDF2
    doc = PyPDF2.PdfFileReader(file_name)

    #PYMUPDF AKA FITZ
    doc2 = fitz.open(file_name)

    # #PDFPLUMBER
    # doc3 = pdfplumber.open(file_name)

    # Find number of pages
    pages = doc.getNumPages()

    # Split pdf object into pages of text
    txt = []
    for i in range(pages):
        #PyPDF2
        current = doc.getPage(i)
        #PyMuPDF
        current2 = doc2.load_page(i)
        # #PyPDFPLumber
        # current3 = doc3.pages[i]

        if current.extractText() != '':
            txt.append(current.extractText())
        elif current2.get_text('text') != '':
            txt.append(current2.get_text('text'))
        # elif current3.extract_text() != '':
        #     txt.append(current.extract_text())
        else:
            txt.append('Could not Read Page')
    #print(txt)

    # Save to variable the file without the "new line" data
    corpus = read_list_pages(txt)

    # Checking the Output: Should be a list of strings containing each individual page of the pdf document
    # Corpus should have trailing newline ('\n') characters stripped off the words
    # print(txt)
    # print("\n")
    # print("\n")
    # print(corpus)

    toked_list = to_sent(corpus)
    # check resulting list  of tokenized pages
    # print("\n")
    # print('\n')
    # print(toked_list)

    keyword = ['expire', 'dated','effective','period','term']

    # Create a List of all keywords and the sentence they are found in
    out_list = []
    for i in range(len(toked_list)):
        # df.loc[i,'Filename'] = file_name
        output = find_sent_with_word(keyword, toked_list[i])
        out_list.append(output)

    # Split List into two lists: the key words, the lines
    keywords = []
    lines = []
    for i in range(0, len(out_list) - 1):
        if not out_list[i]:
            pass
        else:
            keywords.append(out_list[i][0][0])
            lines.append(out_list[i][0][1])
    # print(keywords)
    # print(lines)
    d.append({'File Name': os.path.basename(file_name), 'Keyword': keywords,'Line': lines})
    # ser = pd.Series(d, index = ['File Name','Keyword','Line'])
    # print(ser)

    # df[sum]['Filename'] = ser['File Name']
    # df[sum]['Keyword'] = ser['Keyword']
    # df[sum]['Line'] = ser['Line']
    #df.fillna(os.path.basename(file_name), inplace=True)
    sum = sum + 1

    # List of tuples (all occurences, page number)
    # list_pages = []

    # pattern = r"([^.]*?expire[^.]*\." #+ r'([a-zA-Z]|$)'

    # for i in range(pages):
    #   current_page = doc.getPage(i)
    #   text = current_page.extractText()
    # for line in text:
    #   result = re.search(r""(^|[^a-zA-Z])+ 'expire' +r"([^a-zA-Z]|$")
    #   print(re.findall(pattern,text))
    #   if re.finditer(term, text):
    #       count_page = len(re.findall(pattern,text))
    #       list_pages.append((count_page, i))

    # result
    # print(list_pages)
    # print(text)

# Verifying Output: Should be dataframe with the file name, the key word, and the line it is found
pd.options.display.width = None
pd.options.display.max_columns = None

df = pd.DataFrame(d)
print(df)
df.to_csv('NDA_Exp.csv')

# # writing the application to be run frm the CMD Line
# # Assign the File
# file_name = sys.argv[1]
# doc = PyPDF2.PdfFileReader(file_name)
#
# # Find number of pages
# pages = doc.getNumPages()
#
# # Split pdf object into pages of text
# txt = []
# for i in range(pages):
#     current = doc.getPage(i)
#     txt.append(current.extractText())
#
#
# # Function to Strip Out "new line" data: Reduces "Extra data" that complicates further processing
# def read_list_pages(list_pages):
#     texts = []
#     for word in list_pages:
#         text = word.rstrip('\n')
#         texts.append(text)
#     return texts
#
#
# # Save to variable the file without the "new line" data
# corpus = read_list_pages(txt)
#
#
# # Checking the Output: Should be a list of strings containing each individual page of the pdf document
# # Corpus should have trailing newline ('\n') characters stripped off the words
# # print(txt)
# # print("\n")
# # print("\n")
# # print(corpus)
#
# # Tokenizing the data (Separating each page by sentence)
# def to_sent(page_list):
#     sent_list = []
#     for page in range(len(page_list)):
#         sent_token = nltk.sent_tokenize(page_list[page])
#         sent_list.append(sent_token)
#     return sent_list
#
#
# toked_list = to_sent(corpus)
# # check resulting list  of tokenized pages
# # print("\n")
# # print('\n')
# # print(toked_list)
#
# # Seperate out sentences containing keyword "expire" Store it in "file"
# file = open('testfile.txt', 'w', encoding='utf-8')
# def find_sent_with_word(file, keyword, corpus):
#     keyline = []
#     for line in corpus:
#         # line = line.lower()
#         for key in keyword:
#             result = re.search(r"(^|[^a-z])" + key + r"([^a-z]|$)", line)
#             if result != None:
#                 keypair = (key, line)
#                 keyline.append(keypair)
#                 file.write(line + " ")
#                 break
#             else:
#                 pass
#     return (keyline)
#
# n = len(sys.argv[2])
# keyword = sys.argv[2][1:n-1]
# keyword = keyword.split(',')
#
# # Create a List of all keywords and the sentence they are found in
# out_list = []
# for i in range(len(toked_list)):
#     # df.loc[i,'Filename'] = file_name
#     output = find_sent_with_word(file, keyword, toked_list[i])
#     out_list.append(output)
#
# # Split List into two lists: the key words, the lines
# keywords = []
# lines = []
# for i in range(0, len(out_list) - 1):
#     if not out_list[i]:
#         pass
#     else:
#         keywords.append(out_list[i][0][0])
#         lines.append(out_list[i][0][1])
# # print(keywords)
# # print(lines)
#
# # Create Dataframe of the key words and the line they're found
# import os
#
# df = pd.DataFrame(columns=['Filename', 'Keyword', 'Line'])
# df.loc[:, 'Filename'] = os.path.basename(file_name)
# df['Keyword'] = keywords
# df['Line'] = lines
# df.fillna(os.path.basename(file_name), inplace=True)
#
# # Verifying Output: Should be dataframe with the file name, the key word, and the line it is found
# pd.options.display.width = None
# pd.options.display.max_columns = None
#
# print(df)
# df.to_csv('NDA_Exp.csv')
#
# # print(keywords)
# # print(lines)
# # print(out_list)
# # df = pd.DataFrame(out_list, columns = ['Keyword', 'Line'])
# # print(df)
#
# # term = "expire"
#
# # List of tuples (all occurences, page number)
# # list_pages = []
#
# # pattern = r"([^.]*?expire[^.]*\." #+ r'([a-zA-Z]|$)'
#
# # for i in range(pages):
# #   current_page = doc.getPage(i)
# #   text = current_page.extractText()
#     # for line in text:
#     #   result = re.search(r""(^|[^a-zA-Z])+ 'expire' +r"([^a-zA-Z]|$")
#     #   print(re.findall(pattern,text))
#     #   if re.finditer(term, text):
#     #       count_page = len(re.findall(pattern,text))
#     #       list_pages.append((count_page, i))
#
# # result
# # print(list_pages)
# # print(text)



## Maybe Write it as a Class??

# if __name__ == "__main__":
#
#     # Assign the File
#     # file_name = sys.argv[1]
#     file_name = "C:\\Users\\Kanayo Anagbogu\\Documents\\2021-03-19_CNDA_JJPR LLC.pdf"
#     doc = PyPDF2.PdfFileReader(file_name)
#
#     # Find number of pages
#     pages = doc.getNumPages()
#     print(pages)
#     # Split pdf object into pages of text
#     txt = []
#     for i in range(pages):
#         current = doc.getPage(i)
#         txt.append(current.extractText())
#
#
#     # Function to Strip Out "new line" data: Reduces "Extra data" that complicates further processing
#     def read_list_pages(list_pages):
#         texts = []
#         for word in list_pages:
#             text = word.rstrip('\n')
#             texts.append(text)
#         return texts
#
#
#     # Save to variable the file without the "new line" data
#     corpus = read_list_pages(txt)
#
#
#     # Checking the Output: Should be a list of strings containing each individual page of the pdf document
#     # Corpus should have trailing newline ('\n') characters stripped off the words
#     # print(txt)
#     # print("\n")
#     # print("\n")
#     # print(corpus)
#
#     # Tokenizing the data (Separating each page by sentence)
#     def to_sent(page_list):
#         sent_list = []
#         for page in range(len(page_list)):
#             sent_token = nltk.sent_tokenize(page_list[page])
#             sent_list.append(sent_token)
#         return sent_list
#
#
#     toked_list = to_sent(corpus)
#     # check resulting list  of tokenized pages
#     # print("\n")
#     # print('\n')
#     # print(toked_list)
#
#     # Seperate out sentences containing keyword "expire" Store it in "file"
#
#     file = open('testfile.txt', 'w', encoding='utf-8')
#
#
#     def find_sent_with_word(file, keyword, corpus):
#         keyline = []
#         for line in corpus:
#             # line = line.lower()
#             for key in keyword:
#                 result = re.search(r"(^|[^a-z])" + key + r"([^a-z]|$)", line)
#                 if result != None:
#                     keypair = (key, line)
#                     keyline.append(keypair)
#                     file.write(line + " ")
#                     break
#                 else:
#                     pass
#         return (keyline)
#
#
#     keyword = ['expire', 'dated']
#     # keyword = sys.argv[2]
#     # Create a List of all keywords and the sentence they are found in
#     out_list = []
#     for i in range(len(toked_list)):
#         # df.loc[i,'Filename'] = file_name
#         output = find_sent_with_word(file, keyword, toked_list[i])
#         out_list.append(output)
#
#     # Split List into two lists: the key words, the lines
#     keywords = []
#     lines = []
#     for i in range(0, len(out_list) - 1):
#         if not out_list[i]:
#             pass
#         else:
#             keywords.append(out_list[i][0][0])
#             lines.append(out_list[i][0][1])
#     # print(keywords)
#     # print(lines)
#
#     # Create Dataframe of the key words and the line they're found
#     import os
#
#     df = pd.DataFrame(columns=['Filename', 'Keyword', 'Line'])
#     df.loc[:, 'Filename'] = os.path.basename(file_name)
#     df['Keyword'] = keywords
#     df['Line'] = lines
#     df.fillna(os.path.basename(file_name), inplace=True)
#
#     # Verifying Output: Should be dataframe with the file name, the key word, and the line it is found
#     pd.options.display.width = None
#     pd.options.display.max_columns = None
#
#     print(df)
#     df.to_csv('NDA_Exp.csv')
#
#     # print(keywords)
#     # print(lines)
#     # print(out_list)
#     # df = pd.DataFrame(out_list, columns = ['Keyword', 'Line'])
#     # print(df)
#
#     # term = "expire"
#
#     # List of tuples (all occurences, page number)
#     # list_pages = []
#
#     # pattern = r"([^.]*?expire[^.]*\." #+ r'([a-zA-Z]|$)'
#
#     # for i in range(pages):
#     # current_page = doc.getPage(i)
#     # text = current_page.extractText()
#     # for line in text:
#     #   result = re.search(r""(^|[^a-zA-Z])+ 'expire' +r"([^a-zA-Z]|$")
#     # print(re.findall(pattern,text))
#     # if re.finditer(term, text):
#     # count_page = len(re.findall(pattern,text))
#     # list_pages.append((count_page, i))
#
#     # result
#     # print(list_pages)
#     # print(text)