"""
Author: Konstantinos Lessis
Created: 14.08.2022 
Description: This script contains the function that extract alls keywords, pos, bert and wiki

"""

from .helper.pos import extract_pos_candidates, too_many_single_character_words
from .helper.keybert import calculate_bert_vector, calculate_cosine_similarity
from brain.data_preprocessing.classes.main_class import Lecture, Slide, Keyword
from brain.keyword_extraction.helper.n_gram import set_n_grams, create_n_gram_count_dict, improve_pos_candidates



def keyword_extraction(lecture: Lecture) -> Lecture:
    #----------Extract POS Candidates----------
    slides = lecture.slides
    #lecture.yake_terms = 
    for slide in slides:
        keywords = []
        paragraphs = slide.paragraphs
        for paragraph in paragraphs:
            #Extract Title Keywords
            if paragraphs.index(paragraph) == 0: #TODO: AND IF HAS TITLE:
                pos_keywords_titleparagraph = extract_pos_candidates(paragraph)
                for kw in pos_keywords_titleparagraph:
                    #Filter out
                    if len(kw) > 1 and len(kw.split())<5:
                        if not too_many_single_character_words(kw):
                            keyword = Keyword(kw,True)
                            #Automatically set title keyword as relevant
                            keyword.is_relevant = True
                            keywords.append(keyword)
            #Extract Below Title Keywords
            else:
                pos_keywords_paragraph = extract_pos_candidates(paragraph)
                for kw in pos_keywords_paragraph:
                    #Filter out
                    if len(kw) > 1 and len(kw.split())<5 :
                        if not too_many_single_character_words(kw):
                            keyword = Keyword(kw,False)
                            keywords.append(keyword)
        #Add only unique keywords to the slide keywords             
        unique_keywords = []
        all_pos = []
        for kw in keywords:
            if kw.pos not in all_pos:
                unique_keywords.append(kw)
            all_pos.append(kw.pos)

        slide.keywords = unique_keywords

        #Set bi, tri, four grams for every slide
        set_n_grams(slide)

    #Create dictionary with counts for all pos candidates, bi, tri, four grams
    count_dictionary = create_n_gram_count_dict(lecture)

    for slide in lecture.slides:
        improve_pos_candidates(slide, count_dictionary) 
    

    #For Lecture
    lecture.bert_vector = calculate_bert_vector(lecture.text_for_vector)

    #Create a dictionary {keyword:vector} to colllect the vectors for keywords
    keywords_embedding_dict = {}

    #For Slide
    for slide in slides:
        slide.bert_vector = calculate_bert_vector(slide.text_for_vector)

        #For Keywords
        #If keyword_pos occurs more than once, do not calculate again but take the saved vector
        for keyword in slide.keywords:
            if keyword.pos in keywords_embedding_dict:
                keyword.bert_vector = keywords_embedding_dict[keyword.pos]
            else:
                keyword.bert_vector = calculate_bert_vector(keyword.pos)
                keywords_embedding_dict[keyword.pos] = keyword.bert_vector

    #---------Find out which keywords are relevant----------

    lecture_vector = lecture.bert_vector
    lecture_total_pages = len(lecture.slides)
    valid_pagenumbers = range(1,lecture_total_pages+1)

    for slide in slides:
        #Collect all keywords with their cosine distance as tuples in list (cosine_distance, keyword)
        keyword_to_slide = []
        keyword_to_neighbours = []
        keyword_to_lecture = []
        slide_vector = slide.bert_vector

        #Find neighbouring pages and calculate bert vector
        relevant_pages = [slide.pagenum-1,slide.pagenum, slide.pagenum+1]
        relevant_existing_pages = [pagenumber for pagenumber in relevant_pages if pagenumber in valid_pagenumbers]
        relevant_indices = [pagenumber-1 for pagenumber in relevant_existing_pages]
        #The text of all neighouring pages and the slide the keyword is on
        neighbour_text = ""
        for index in relevant_indices:
            slide_text = slides[index].text_for_vector
            neighbour_text += slide_text

        #Calculate the vector for the whole text
        slide_neighbour_vector = calculate_bert_vector(neighbour_text)

        for keyword in slide.keywords:
            #Compare Keyword To Slide Text with Cosine Similarity
            cosine_similarity_slide = calculate_cosine_similarity(keyword.bert_vector,slide_vector)
            keyword.cos_sim_slide = cosine_similarity_slide[0][0].item()
            keyword_to_slide.append((keyword.cos_sim_slide ,keyword))
            
            #Compare Keyword To Slide and Slideneighbours Text with Cosine Similarity
            cosine_similarity_slide_neighbour = calculate_cosine_similarity(keyword.bert_vector,slide_neighbour_vector)
            keyword.cos_sim_neighbour = cosine_similarity_slide_neighbour[0][0].item()
            keyword_to_neighbours.append((keyword.cos_sim_neighbour,keyword))

            #Compare Keyword To Slide and Slideneighbours Text with Cosine Similarity
            cosine_similarity_lecture = calculate_cosine_similarity(keyword.bert_vector,lecture_vector)
            keyword.cos_sim_lecture = cosine_similarity_lecture[0][0].item()
            keyword_to_lecture.append((keyword.cos_sim_lecture,keyword))
            
         #For every slide and for every comparison take the 3 most similar    

        keyword_to_slide = sorted(list(set(keyword_to_slide)),key=lambda tup: tup[0], reverse = True)
        
        #Choos which top_n to mark as relevant
        top_n_to_mark_relevant = 5

        #If the list of keywords is smaller than 3 mark everything as as relevant
        if len(keyword_to_slide) >= top_n_to_mark_relevant:
            for k in keyword_to_slide[:top_n_to_mark_relevant]:
                k[1].is_relevant = True
        else:
            for k in keyword_to_slide:
                k[1].is_relevant = True

        keyword_to_neighbours = sorted(list(set(keyword_to_neighbours)), key=lambda tup: tup[0], reverse = True)

        if len(keyword_to_neighbours) >= top_n_to_mark_relevant:
            for k in keyword_to_slide[:top_n_to_mark_relevant]:
                k[1].is_relevant = True
        else:
            for k in keyword_to_neighbours:
                k[1].is_relevant = True


        keyword_to_lecture = sorted(list(set(keyword_to_lecture)),key=lambda tup: tup[0], reverse = True)

        if len(keyword_to_lecture) >= top_n_to_mark_relevant:
            for k in keyword_to_lecture[:top_n_to_mark_relevant]:
                k[1].is_relevant = True
        else:
            for k in keyword_to_lecture:
                k[1].is_relevant = True

    return lecture
