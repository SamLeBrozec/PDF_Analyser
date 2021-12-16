#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 14:46:47 2021

Simple pdf analyser in order to count occurence of words in a job offer
The punctuations character are removed
The most link words are removed 
save a sorted dictionnary in a csv file


@author: samuel
"""

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

import sys



def convert_pdf_to_txt(path):
    """
    Convert pdf file in str variable
    
    Parameters
    ---------- 
    path : str
        path to the pdf file to convert
    
    Returns
    -------
    txt : str
        contains the text inculde in the pdf file
        
    """
    
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    # codec = 'utf-8'
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


def clean_text(text, punctList = [',',';',':','.','!','/','\n','(',')',"’",'-','_',"'",'"']):
    """
    replace punctuation chrarcters from of a text by the space ' ' character
    
    Parameters
    ---------- 
    text : str
        text to clean 
    
    punctList : list
        list of charchter to be removed from the text 
    
    Returns
    -------
    outText : str
        cleaned text
        
    """
        
    for ponctuation in punctList:
        text = text.replace(ponctuation," ")
    
    text = ''.join(i for i in text if not i.isdigit())
    text = text.split()
    text  = [''.join(i for i in t if i.isalpha()) for t in text]
    
    outText = text 
    
    return outText

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

def removemotliaison(dic, wordList = ['de','des','les','la','le','au','sur','dans','ce','cette','et','pour','que','qui','à','du','l','d',
                'ou','notre','en','un','une','est','vous','votre','plus','ses','son','ces','avec','aux','vos',
                'il','elle','on','nos','êtes','par','lors','pas']):
    
    
    
    for liaison in wordList :
        if liaison in dic:
            dic.pop(liaison)
    return dic



file = sys.argv[1]
fileout = file.split('.pdf')[0]+'.csv'

text = convert_pdf_to_txt(file)
textList = clean_text(text)
dic =  count(textList)
dic = sort(dic)
dic = removemotliaison(dic)

with open(fileout, 'w') as f:
    for key in dic.keys():
        f.write("%s,%s\n"%(key,dic[key]))



print(dic)
