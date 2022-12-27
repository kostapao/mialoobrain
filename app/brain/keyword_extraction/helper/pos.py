"""
Author: Konstantinos Lessis
Created: 14.08.2022 
Description: This script contains the function that extracts part of speech candidates (POS) from the slide text

"""

import nltk
from nltk import ngrams
from typing import List
from brain.data_preprocessing.classes.main_class import Slide
from nltk.corpus import stopwords


def extract_pos_candidates(text: str) -> List:
    """Extract POS candidates of a string"""
    words = nltk.word_tokenize(text)
    #Tag each word with corresponding Part of Speech
    tagged = nltk.pos_tag(words)
    #print('POS tagged words= ',tagged)
    # Paper Source: Keyword Extraction from Educational Video Transcripts Using NLP techniques
    chunkGram = r"""chunk: {<JJ|JJR|JJS> *(<NNP> + <POS> *)?<NN|NNS|NNP|NNPS>+}"""
    chunkParser = nltk.RegexpParser(chunkGram)
    #Parsing
    chunked = chunkParser.parse(tagged)
    #Get Text out of chunks
    pos_candidates = []
    for a in chunked:
        if isinstance(a, nltk.tree.Tree):
            if a.label() == "chunk":
                pos_candidates.append(" ".join([lf[0] for lf in a.leaves()]))
    return pos_candidates



def too_many_single_character_words(candidate: str) -> bool:
    """If a candidate has more than one substring that contains only one character return True, this serves to omit mathimatical strings"""
    candidate_substrings = candidate.split()
    single_character_counter = 0
    for sub in candidate_substrings:
        if len(sub) == 1:
            single_character_counter +=1
    if single_character_counter > 1:
        return True
    else:
        False
        