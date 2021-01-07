#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Load the "autoreload" extension
get_ipython().run_line_magic('load_ext', 'autoreload')
# Always reload all modules (except those excluded by %aimport)
get_ipython().run_line_magic('autoreload', '2')
import os
import sys
from pathlib import Path


# add the 'src' directory as the one we can import from
src_dir = str(Path(os.getcwd(), '..', 'src'))
sys.path.append(src_dir)

#Input data folder path
DATA_PATH_IN=Path(os.getcwd(), '..', 'data','input')

#DATA_PATH 
DATA_PATH=Path(os.getcwd(),'..','data')

import utils

import validators


# In[2]:


#Provide pdf file name or url. If no filename or url is provided ask again
#check if the provided is an url or pdf file. If none, print error message

file_url=''
file_url=input('Enter pdf filename or an URL: \n')

while file_url == '':
    file_url = input('No pdf filename or url provided, please provide one: \n')
    
if validators.url(file_url) == True:
    text=utils.convert_url_to_string(file_url)
elif file_url[-3:]=='pdf':
    text=utils.convert_pdf_to_string(DATA_PATH_IN/file_url)
    print('Total number of pages in this PDF are: {}'.format(utils.total_num_pages(DATA_PATH_IN,file_url))) # will give total number of pages in pdf
else:
    print ("Not a valid URL or Not a PDF file")


# ### Keywords

# In[7]:


#Gensim keywords
kws,scores,df=utils.keywords_scores(text)
kws


# ### Keyphrases

# In[4]:


key_phr,key_phr_score_df=utils.key_phrases_rake(text)
key_phr


# ### Summaries/Phrases

# In[5]:


summary,summary_list=utils.key_summaries(text)
summary_list


# In[ ]:




