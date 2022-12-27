from nltk import ngrams
from typing import List, Tuple,Dict
from brain.data_preprocessing.classes.main_class import Slide, Lecture, Keyword
from nltk.corpus import stopwords
from brain.keyword_extraction.helper.pos import extract_pos_candidates


stop_words = stopwords.words('english')



#lecture_text.count(key)


def tuple_to_string(t: Tuple) -> str:
    string_version = " ".join(t)
    return string_version



def get_slide_tokens(slide: Slide) -> Slide:
    tokens_no_stopwords = []
    for paragraph in slide.paragraphs:
        tokens = list(ngrams(paragraph.split(), 1))
        for token in tokens:
            if token[0] not in stop_words:
                tokens_no_stopwords.append(token[0])
    slide.tokens = list(set(tokens_no_stopwords))
    return slide.tokens

def get_slide_bigrams(slide: Slide) -> List[str]:
    bi_grams_no_stopwords = []
    for paragraph in slide.paragraphs:
        bi_grams = list(ngrams(paragraph.split(), 2))
        for bi_gram in bi_grams:
            if bi_gram[0] not in stop_words and bi_gram[-1] not in stop_words:
                bi_grams_no_stopwords.append(tuple_to_string(bi_gram))
    slide.bi_grams = list(set(bi_grams_no_stopwords))
    return slide.bi_grams


def get_slide_trigrams(slide: Slide) -> List[str]:
    tri_grams_no_stopwords = []
    for paragraph in slide.paragraphs:
        tri_grams = list(ngrams(paragraph.split(), 3))
        for tri_gram in tri_grams:
            if tri_gram[0] not in stop_words and tri_gram[-1] not in stop_words:
                tri_grams_no_stopwords.append(tuple_to_string(tri_gram))
    slide.tri_grams = list(set(tri_grams_no_stopwords))
    return slide.tri_grams


def get_slide_fourgrams(slide: Slide) -> List[str]:
    four_grams_no_stopwords = []
    for paragraph in slide.paragraphs:
        four_grams = list(ngrams(paragraph.split(), 4))
        for four_gram in four_grams:
            if four_gram[0] not in stop_words and four_gram[-1] not in stop_words:
                four_grams_no_stopwords.append(tuple_to_string(four_gram))
    slide.four_grams = list(set(four_grams_no_stopwords))
    return slide.four_grams


def create_n_gram_count_dict(lec: Lecture) -> Dict:
    n_gram_count_dict ={}
    lecture_text = lec.text_for_vector
    for slide in lec.slides:
        for bi_gram in slide.bi_grams:
            if bi_gram not in n_gram_count_dict:
                n_gram_count_dict[bi_gram] = lecture_text.count(bi_gram)
        for tri_gram in slide.tri_grams:
            if tri_gram not in n_gram_count_dict:
                n_gram_count_dict[tri_gram] = lecture_text.count(tri_gram)
        for four_gram in slide.four_grams:
            if four_gram not in n_gram_count_dict:
                n_gram_count_dict[four_gram] = lecture_text.count(four_gram)
        for keyword in slide.keywords:
            if keyword.pos not in n_gram_count_dict:
                n_gram_count_dict[keyword.pos] = lecture_text.count(keyword.pos)
    lec.n_gram_count_dict = n_gram_count_dict
    return lec.n_gram_count_dict


def find_tri_grams_where_pos_bi_grams(slide: Slide, count_dictionary = Dict) -> None:
    """for every bi_gram created by pos get trigrams where bi_gram is inside, if tri gram occurs more often than bi_gram, include in keywords"""
    tri_grams_to_keywords = []
    for kw in slide.keywords:
        if len(kw.pos.split()) == 2:
            count_kw_pos = count_dictionary[kw.pos]
            for tri_gram in slide.tri_grams:
                if kw.pos in tri_gram:
                    if count_dictionary[tri_gram] > count_kw_pos:
                        tri_grams_to_keywords.append(tri_gram)
    improved_keyword_set = slide.keywords
    for tri_gram in tri_grams_to_keywords:
        keyword = Keyword(tri_gram,False)
        improved_keyword_set.append(keyword)
    slide.keywords = improved_keyword_set
        




def find_bi_grams_in_pos_tri_grams(slide: Slide, count_dictionary = Dict) -> None:
    """for every tri_gram created by pos, get bi_grams that are inside, if bi_gram occurs more often than tri_gram, include in keywords"""
    bi_grams_to_keywords = []
    for kw in slide.keywords:
        if len(kw.pos.split()) == 3:
            count_kw_pos = count_dictionary[kw.pos]
            for bi_gram in slide.bi_grams:
                if bi_gram in kw.pos:
                    if count_dictionary[bi_gram] > count_kw_pos:
                        bi_grams_to_keywords.append(bi_gram)

    improved_keyword_set = slide.keywords
    for bi_gram in bi_grams_to_keywords:
        keyword = Keyword(bi_gram,False)
        improved_keyword_set.append(keyword)
    slide.keywords = improved_keyword_set


def find_four_grams_where_pos_tri_grams(slide: Slide, count_dictionary = Dict) -> None:
    """for every tri_gram created by pos, get four_grams where tri_gram is inside, if four_gram occurs more often than tri_gram, include in keywords"""
    four_grams_to_keywords = []
    for kw in slide.keywords:
        if len(kw.pos.split()) == 3:
            count_kw_pos = count_dictionary[kw.pos]
            for four_gram in slide.bi_grams:
                if kw.pos in four_gram:
                    if count_dictionary[four_gram] > count_kw_pos:
                        four_grams_to_keywords.append(four_gram)
    improved_keyword_set = slide.keywords
    for four_gram in four_grams_to_keywords:
        keyword = Keyword(four_gram,False)
        improved_keyword_set.append(keyword)
    slide.keywords = improved_keyword_set

def find_tri_grams_in_pos_four_grams(slide: Slide, count_dictionary = Dict) -> None:
    """for every four_gram created by pos, get tri_grams that are inside, if four_gram occurs more often than tri_gram, include in keywords"""
    tri_grams_to_keywords = []
    for kw in slide.keywords:
        if len(kw.pos.split()) == 4:
            count_kw_pos = count_dictionary[kw.pos]
            for tri_gram in slide.tri_grams:
                if tri_gram in kw.pos:
                    if count_dictionary[tri_gram] > count_kw_pos:
                        tri_grams_to_keywords.append(tri_gram)
    improved_keyword_set = slide.keywords
    for tri_gram in tri_grams_to_keywords:
        keyword = Keyword(tri_gram,False)
        improved_keyword_set.append(keyword)
    slide.keywords = improved_keyword_set




def set_n_grams(slide: Slide):
    slide.bi_grams = get_slide_bigrams(slide)
    slide.tri_grams = get_slide_trigrams(slide)
    slide.four_grams = get_slide_fourgrams(slide)



def improve_pos_candidates(slide: Slide, count_dictionary = Dict) -> None:
    find_tri_grams_where_pos_bi_grams(slide, count_dictionary)
    find_bi_grams_in_pos_tri_grams(slide, count_dictionary)
    find_four_grams_where_pos_tri_grams(slide, count_dictionary)
    find_four_grams_where_pos_tri_grams(slide, count_dictionary)



