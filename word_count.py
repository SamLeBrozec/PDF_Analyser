#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 14:46:47 2021

@author: samuel
"""

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

import sys



def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    # device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    device = TextConverter(rsrcmgr, retstr,  laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()
    text = text.lower()
    fp.close()
    device.close()
    retstr.close()
    return text


def clean_text(text):
    
    
    
    for ponctuation in [',',';',':','.','!','/','\n','(',')',"’",'-','_',"'",'"']:
        text = text.replace(ponctuation," ")
    
    text = ''.join(i for i in text if not i.isdigit())
    text = text.split()
    text  = [''.join(i for i in t if i.isalpha()) for t in text]
    
     
    
    return text

def count(L):
    d = dict()
# Loop through each line of the file
    for word in L:
        # Check if the word is already in dictionary
        if word in d:
            # Increment count of word by 1
            d[word] = d[word] + 1
        else:
            # Add the word to dictionary with count 1
            d[word] = 1
    return d

def sort(x):
    return dict(sorted(x.items(), key=lambda item: item[1],reverse = True))

def removemotliaison(dic):
    for liaison in ['de','des','les','la','le','au','sur','dans','ce','cette','et','pour','que','qui','à','du','l','d',
                    'ou','notre','en','un','une','est','vous','votre','plus','ses','son','ces','avec','aux','vos',
                    'il','elle','on','nos','êtes','par','lors','pas']:
        if liaison in dic:
            dic.pop(liaison)
    return dic



# print(sys.argv)
file = sys.argv[1]
# '/home/samuel/Documents/Samuel/CV/GENVIA/Oct21_IngenieurModelisationStack.pdf'
fileout = file.split('.pdf')[0]+'.csv'
# file ='/home/samuel/Documents/Samuel/CV/GENVIA/CV_LE_BROZEC.pdf'

text = convert_pdf_to_txt(file)
textList = clean_text(text)
dic =  count(textList)
dic = sort(dic)
dic = removemotliaison(dic)

with open(fileout, 'w') as f:
    for key in dic.keys():
        f.write("%s,%s\n"%(key,dic[key]))



print(dic)
