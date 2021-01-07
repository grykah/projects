## Python Script: Keyword_and_Keyphrases_from_PDF_or_URL
## This script takes a PDF file or an URL and returns keywords and keyphrases

## Details: Input an article using PDF file or an URL. If article is not in PDF format or not a valid URL an error will be displayed. The output will be the number of pages(for PDF files), top 10 keywords from the article, top 10 important phrases from the article and a summary of the article. 

Steps:
1. Enter PDF or URL
2. Check if it's a PDF file or a valid URL. 
    Continue if they are; Exit if they aren't.
3. Convert PDF file/URL into text using PDFMiner library
4. Pass the text into gensim's keyword module to extract keywords. 
5. Pass the text into RAKE module of nlth_rake to extract keyphrases.
6. Pass the text into gensim's summarization's summarizer function to extract summary.

### Functions in util.py file

1. convert_pdf_to_string(file_path):
    Input: file_path(str): currently the file has to be in DATA_PATH_IN folder
    Output: text (str): text from the pdf file provided

2. convert_url_to_string(url_link):
    Input: url_link(str): Any url link that ends with html, com etc.(Validator module is used to verify url's validity)
    Output: text(str): text from the url provided
    
3. weightage(word,text,number_of_documents=1):
     Input: word (str): whose tf-idf is to be found
            text (str): text returned from convert_url_to_string or convert_pdf_to_string func
            number_of_documents (int): set to 1 as we only have one text for entire pdf file or url
     Output: number_of_times_word_appeared (int),
             tf (float),
             idf (float),               
             tf-idf (float)
             This script is just utilizing 'number_of_times_word_appeared' and tf-idf for output
             
4. keywords_scores(text, num_top_kws=10,save_kws_file=False)
     Input: text (str): text returned from convert_url_to_string or convert_pdf_to_string func
            num_top_kws: Number of keywords to be returned. Default=10
            save_kws_file (bool): True if a csv file needs to be saved for saving the output. The default is False
    Output: keyword_list(list): List of top num_top_kws keywords
            keyword_score_dict (dict): Dictionary with keywords as keys and  score (tf-idf) as values
            df (dataframe): Dataframe with keywords, number of times the kw  appeared in the text, keyword, tf-idf score
            
5. key_phrases_rake(text,num_top_phr=10, save_phr_file=False)
     Input: text (str): text returned from convert_url_to_string or convert_pdf_to_string func
            num_top_phr: Number of phrases to be returned. Default=10
            save_phr_file (bool):True if a csv file needs to be saved for saving the output. The default is False
        
    Output: phrase_list (list): List of top num_top_phr phrases
            df (dataframe): Dataframe with scores (scores returned using  nltk_rank module and phrases)
            
6. key_summaries(text,save_summ_file=False,word_count=200):
     Input: text (str): text returned from convert_url_to_string or convert_pdf_to_string func
            save_summ_file (bool): True if a csv file needs to be saved for saving the output. The default is False
            word_count (int): Total number of words present in the summary 
    Output: sentences (str): summary in a few sentences (200 words)
            sentences_list (list): All the sentences as a list  
    
7. text_preprocess(text):
      Input: text (str): text returned from convert_url_to_string or convert_pdf_to_string func
            
     


