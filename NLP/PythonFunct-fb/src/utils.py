#!/usr/bin/env python
# coding: utf-8

#importing modules
import pandas as pd
import textract
import numpy as np
import nltk
import PyPDF2
import re

# get pdf as string
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

##
from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords
from rake_nltk import Rake
#nltk.download('averaged_perceptron_tagger')
#nltk.download('brown')

#for url
from urllib.request import urlopen
from bs4 import BeautifulSoup

import logging


#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    #level=logging.INFO)
###########################################################################################################################

def convert_pdf_to_string(file_path):
    output_string = StringIO()
    with open(file_path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
    if output_string.getvalue() != "":
        output_string = output_string
    else:
        output_string = textract.process('http://bit.ly/epo_keyword_extraction_document', method='tesseract', language='eng')

    return(output_string.getvalue())
##########################################################################

def convert_url_to_string(url_link):
    html = urlopen(url_link).read()
    soup = BeautifulSoup(html, features='html.parser')
    
    #kill all script and style elements
    for script in soup(['script','style']):
        script.extract()
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return(text)
###########################################################################

def weightage(word,text,number_of_documents=1):
    word_list = re.findall(word,text)
    number_of_times_word_appeared =len(word_list)
    tf = number_of_times_word_appeared/(1+float(len(text)))
    idf = np.log((number_of_documents)/(1+float(number_of_times_word_appeared)))
    tf_idf = tf*idf
    return number_of_times_word_appeared,tf,idf ,tf_idf
#######################################################
#TF-IDF is Term Freq - Inverse Document Frequency
# TF: How freq is a term in a doc.Total num of term/total num of terms in the document
# IDF: How important the term in. Weigh down most freq terms (is,of, that) and scale up rare terms
     #: log_e(Total number of documents/Num of documents with term in it)
####################################################### 

def total_num_pages(INPUT_DATA_PATH,filename):
    pdfFileObj = open(INPUT_DATA_PATH/filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    return pdfReader.numPages
########################################################

def keywords_scores(text, num_top_kws=10,save_kws_file=False):
    extracted_keywords=keywords(text, lemmatize=True).split('\n')
    
    df = pd.DataFrame(list(set(extracted_keywords)),columns=['keywords'])  #Dataframe with unique keywords to avoid repetition in rows

    df['Num_of_Appearances'] = df['keywords'].apply(lambda x: weightage(x,text)[0])
    
    df['tf_idf'] = df['keywords'].apply(lambda x: weightage(x,text)[3])

    df = df.sort_values('tf_idf',ascending=True).reset_index()
    df = df.head(num_top_kws)
    if save_kws_file==True:
        df.to_csv(DATA_PATH/'output/Keywords.csv')
    keyword_list= list(df['keywords'])
    keyword_score_dict= df.set_index('keywords')['tf_idf'].to_dict()
    return  keyword_list,keyword_score_dict,df
#########################################################

def key_phrases_rake(text,num_top_phr=10, save_phr_file=False):
    r = Rake()
    r.extract_keywords_from_text(text_preprocess(text))
    phrases = r.get_ranked_phrases_with_scores()

    df = pd.DataFrame(phrases,columns=['score','Phrase'])
    df = df.head(num_top_phr)
    df = df.sort_values('score',ascending=False)
    if save_phr_file==True:
        df.to_csv(DATA_PATH/'keywords_phrases.csv')
    phrase_list=list(df['Phrase'])
    return phrase_list, df
##########################################################

def key_summaries(text,save_summ_file=False,word_count=200):
    summary=summarize(str(text),word_count=word_count)
    sentences=[]
    for sent in summary.split('\n'):
        sentences.append(sent.capitalize())
    sentences = ' '.join(sentences)
    sentences_list = summary.split('\n')
    return sentences,sentences_list  

################################################################

def text_preprocess(text):
    # clean text
    text = re.sub("\\d|\\W", " ", text) #replace all numbers and any letter that is not a character (a-z or A-Z) with a space ' '
    #text = re.sub("[^a-zA-Z0-9 -]", " ", text) #replace all non alphanumeric chars with a space ' '
    text = text.strip('\n') #stip off all new line characters
    text = text.strip('\t')
    # make all same case
    text = text.lower()
    return text 