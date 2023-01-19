
import sys
import os
from brain.data_preprocessing.classes.main_class import Lecture
from brain.data_preprocessing.preprocess import data_preprocessing
from brain.data_preprocessing.textprocess import text_processing
from brain.keyword_extraction.keywordextraction import keyword_extraction
from brain.wikipedia_extraction.wikipediaextraction import wikipedia_extraction
from brain.wikipedia_extraction.helper.wikipedia_prep import create_ranked_clusters, create_search_batches
from brain.mindmap_creation.connect import connect
from brain.mindmap_creation.nodes_edges import get_nodes_edges


filtest_file = "/Users/kosta/Documents/15_Test_Lectures/3_Clustering.pdf"


async def main(file):
    """Use for fastapi"""
    a = data_preprocessing(file)
    b = text_processing(a)
    c = keyword_extraction(b)
    d = create_ranked_clusters(c)
    e = create_search_batches(d)
    f = wikipedia_extraction(e)
    g = connect(f)
    h = get_nodes_edges(g)
    return h




def main_local(file):
    """Use for local testing"""
    a = data_preprocessing(file)
    b = text_processing(a)
    c = keyword_extraction(b)
    d = create_ranked_clusters(c)
    e = create_search_batches(d)    
    f = wikipedia_extraction(e)
    g = connect(f)
    h = get_nodes_edges(g)
    return h





if __name__ == "__main__":
    print(main_local(filtest_file))
    #connect(lec)
    #this is the test
