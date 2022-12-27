"""
Author: Konstantinos Lessis
Created: 20.10.2022 
Description: This script contains the function that does all the Wikipedia related stuff

"""

from typing import List
from brain.data_preprocessing.classes.main_class import Lecture, Keyword
import requests
from brain.wikipedia_extraction.helper.wikipedia_prep import kw_pos_to_kw_mapper, create_ranked_clusters, create_search_batches
from brain.wikipedia_extraction.helper.wikipedia_api import get_wikipedia_titles  






def wikipedia_extraction(lecture: Lecture) -> Lecture:
    map_to_kw_object_dict = kw_pos_to_kw_mapper(lecture)
    search_values = list(map_to_kw_object_dict.keys())
    wikipedia_titles = get_wikipedia_titles(search_values)
    map_wiki_titles = dict(zip(search_values, wikipedia_titles))
    
    #Set wiki_title for every keyword
    for kw_pos in search_values:
        wiki_title = map_wiki_titles[kw_pos]
        related_kw_objects = map_to_kw_object_dict[kw_pos]
        for kw in related_kw_objects:
            kw.wiki_title = wiki_title
    return lecture


   # return lecture





#For the Top_N get all the wikipedia articles, PARALLELIZE!

# def get_wikipedia_article(search_term):
#     url = "https://en.wikipedia.org/w/api.php"+
#     pass




# import requests

# S = requests.Session()

# URL = "https://www.mediawiki.org/w/api.php"

# PARAMS = {
#     "action": "query",
#     "prop": "revisions",
#     "titles": "API|Main Page",
#     "rvprop": "timestamp|user|comment|content",
#     "rvslots": "main",
#     "formatversion": "2",
#     "format": "json"
# }

# R = S.get(url=URL, params=PARAMS)
# DATA = R.json()

# PAGES = DATA["query"]["pages"]

# for page in PAGES:
#     print(page["revisions"])



#Get the 




#format=json&action=query&prop=extracts|pageimages&exintro&explaintext&generator=search&gsrsearch=intitle:planet%20mars&gsrlimit=1&redirects=1