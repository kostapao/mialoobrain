"""
Author: Konstantinos Lessis
Created: 20.10.2022 
Description: This script contains the function that does all the Wikipedia related stuff

"""

from typing import List
from brain.data_preprocessing.classes.main_class import Lecture, Keyword, WikiSearch, WikiArticle
import requests
from brain.wikipedia_extraction.helper.wikipedia_prep import kw_pos_to_kw_mapper, create_ranked_clusters, create_search_batches
from brain.wikipedia_extraction.helper.wikipedia_query import get_wikipedia_search_results
from brain.keyword_extraction.helper.keybert import calculate_bert_vector, calculate_cosine_similarity
from brain.wikipedia_extraction.helper.wikipedia_links import get_wikipedia_links
from brain.wikipedia_extraction.helper.wikipedia_extracts import get_wikipedia_extracts


def wikipedia_extraction(lecture: Lecture) -> Lecture:
    map_to_kw_object_dict = kw_pos_to_kw_mapper(lecture)
    #search_values = [item for sublist in lecture.search_clusters[:3] for item in sublist]
    #search_values = list(map_to_kw_object_dict.keys())
    search_values = lecture.search_clusters[0]
    #Creat WikiSearch objects
    wiki_results = get_wikipedia_search_results(search_values, 3)
    #Get Top N Results from Wikipedia
    wiki_searches = [WikiSearch(kw, search_results) for kw,search_results in wiki_results.items() if len(search_results)>0]
    wiki_articles = []
    #If the wiki title similarity is equal or higher than the keyword similarity, get links from those wiki titles
    for wiki_search in wiki_searches:
        #Take the already calculated value from the firs keyword in the mapping dictionary
        kw_sim = map_to_kw_object_dict[wiki_search.source_keyword][0].cos_sim_lecture
        first_wiki_result = wiki_search.get_first_result
        #Create WikiArticle object
        wiki_article = WikiArticle(first_wiki_result)
        wiki_article.source_keyword = wiki_search.source_keyword
        wiki_article.source_search_results = wiki_search.search_results
        wiki_title_emb = calculate_bert_vector(wiki_article.wiki_title)
        wiki_title_sim = calculate_cosine_similarity(wiki_title_emb,lecture.bert_vector)[0].item()
        wiki_article.title_lecture_similarity = wiki_title_sim 
        if wiki_title_sim >= kw_sim:
            wiki_article.keep = True
        else:
            wiki_article.keep = False
        wiki_articles.append(wiki_article)

    #Get links from the wiki titles that have keep = True meaning that their similarity score is higher or equal the keeyword similarity score
    wiki_titles_get_links = []
    for wiki_article in wiki_articles:
        if wiki_article.keep:
            wiki_titles_get_links.append(wiki_article.wiki_title)
    links_dict = get_wikipedia_links(wiki_titles_get_links)
    all_links = []
    for wiki_article in wiki_articles:
        if wiki_article.keep:
            wiki_article.links = links_dict[wiki_article.wiki_title]
            for link in wiki_article.links:
                all_links .append(link)
    # for wiki_article in wiki_articles:
    #     #Check out if the search results of the discarded ones are part of the links that have been kept 
    #     if wiki_article.keep == True:
    #         print("Kept: "+wiki_article.wiki_title)
    # for wiki_article in wiki_articles:
    #     #Check out if the search results of the discarded ones are part of the links that have been kept 
    #     if wiki_article.keep == False:
    #         print("Not Kept: "+wiki_article.wiki_title )
    for wiki_article in wiki_articles:
        #Check out if the search results of the discarded ones are part of the links that have been kept 
        if wiki_article.keep == False:
            for search_result in wiki_article.source_search_results:
                #If one of the search result is in the links, select that linked article as the wiki title and keep the wiki article
                if search_result in all_links:
                    #in case it is the first result that was already looked at before, not many changes need to be done
                    #print("Was Not Kept but now keep because of: ", search_result)
                    if search_result == wiki_article.wiki_title:
                        wiki_article.keep = True
                    else:
                        #Otherwise the wiki title needs to be changed and the similarity score calculated again
                        wiki_article.wiki_title = search_result
                        wiki_title_emb = calculate_bert_vector(wiki_article.wiki_title)
                        wiki_title_sim = calculate_cosine_similarity(wiki_title_emb,lecture.bert_vector)[0].item()
                        wiki_article.title_lecture_similarity = wiki_title_sim
                        wiki_article.keep = True
                    break
    
    #IMPOROVE THE PROCESS HERE
    #    -Get Summaries
    #    -Rank etc.
    ##########################

    #For every keyword set the wiki_title

    for wiki_article in wiki_articles:
        if wiki_article.keep == True:
            for keyword_object in map_to_kw_object_dict[wiki_article.source_keyword]:
                keyword_object.wiki_title = wiki_article.wiki_title
                keyword_object.wiki_title_sim_lecture = wiki_article.title_lecture_similarity

    return lecture
        



    # final_wiki_articles = []
    # for wiki_article in wiki_articles:
    #     if wiki_article.keep == True:
    #         final_wiki_articles.append(wiki_article.wiki_title)
    # final_wiki_articles = sorted(list(set(final_wiki_articles)))
    # print(final_wiki_articles)
    # print(len(final_wiki_articles))



