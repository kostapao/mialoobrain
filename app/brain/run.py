
import sys
import os
from brain.data_preprocessing.preprocess import data_preprocessing
from brain.data_preprocessing.textprocess import text_processing
from brain.keyword_extraction.keywordextraction import keyword_extraction
from brain.wikipedia_extraction.wikipediaextraction import wikipedia_extraction
from brain.wikipedia_extraction.helper.wikipedia_prep import create_ranked_clusters, create_search_batches
from brain.mindmap_creation.connect import connect


filtest_file = "/Users/kosta/Documents/10_mialoo/app/script/data/4_Classification.pdf"


async def main(file):
    """Use for fastapi"""
    a = data_preprocessing(file)
    b = text_processing(a)
    c = keyword_extraction(b)
    d = wikipedia_extraction(c)
    e = connect(d)
    return e




def main_local(file):
    """Use for local testing"""
    a = data_preprocessing(file)
    b = text_processing(a)
    c = keyword_extraction(b)
    d = create_ranked_clusters(c)
    e = create_search_batches(d)
    # d = wikipedia_extraction(c)
    # e = connect(d)
    return e





if __name__ == "__main__":
    clusters = main_local(filtest_file)
    for cluster in clusters:
        print(cluster)
        print(20* "*")
    #connect(lec)
    #this is the test