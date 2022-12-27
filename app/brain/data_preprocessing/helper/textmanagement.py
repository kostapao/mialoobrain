"""
Author: Konstantinos Lessis
Created: 05.08.2022
Description: File containing functions that are needed to clean the text of the slides
"""
import timeout_decorator
import math
import nltk
from nltk.corpus import stopwords
import random
import re
from typing import Dict, List
import os
import shutil


def long_substr(data):
    """In a list of string find longest common substring, used to identify footnotes"""
    def is_substr(find, data):
        find = str(find)
        if len(data) < 1 and len(find) < 1:
            return False
        for i in range(len(data)):
            if find not in data[i]:
                return False
        return True
    substr = ''
    if len(data) > 1 and len(data[0]) > 0:
        for i in range(len(data[0])):
            for j in range(len(data[0])-i+1):
                if j > len(substr) and is_substr(data[0][i:i+j], data):
                    substr = data[0][i:i+j]
    return substr


@timeout_decorator.timeout(60)
def get_footnotes(lecturetext: List,threshold = 0.8) -> Dict:
    """Takes a list of strings. whereas each string contains the 
    text of a slide and returns substrings that occure so often that is is assumed they are head- and footnotes"""
    #List to add strings that are common between lecture slides
    try:
        common_strings = []
        #English stopwords
        sw_nltk = stopwords.words('english')
        #range(x) times pick to slides from the whole lecture set and find longest common string
        for k in range(4):
            global random_slides
            #Remove newline characters and consecutive spaces from text
            #lecturetext = [clean_ocr(str(i)) for i in lecturetext]
            #pick two random slides (actually their text)
            random_slides = [randomslide for randomslide in random.sample(lecturetext,2)]
            #Find longest common string, remove the string from first slide so the next longest can be detected until len(longest) = 3
            while True:
                longest = long_substr(random_slides).strip()
                if len(longest) > 3:
                    common_strings.append(longest)
                    #remove lon
                    new_string = random_slides[0].replace(longest,"")
                    random_slides[0] = new_string
                else:
                    break
        #remove duplicate common strings so the next longest can be detected
        common_strings = set(common_strings)
        #list of final headers and footnotes
        header_footnotes = []
        candidate_count = {}
        #Loop through canidates and check wether they are just substrings of words, if this is the case do not count them
        #Check: If the character before or after is a letter, do not add, still add if candidate is in the beginning or end of text
        for candidate in common_strings:
            counter = 0
            for slide in lecturetext:
                #beginning
                if candidate in slide and slide.index(candidate) == 0: #and not slide[slide.index(candidate)-1].isalpha() and not slide[slide.index(candidate)-1].isalpha():
                    counter +=1
                #end
                elif candidate in slide and slide.index(candidate)+len(candidate) == len(slide):
                    counter +=1
                elif candidate in slide and not slide[slide.index(candidate)-1].isalpha() and not slide[slide.index(candidate)+len(candidate)].isalpha():
                    counter+=1
                else:
                    pass
            #if the candidate occures on more than x% of the slides, it is seen as heder/footnote, also do not add stopwords
            if counter >= math.floor(len(lecturetext)*threshold) and candidate not in sw_nltk:
                header_footnotes.append(candidate)
            candidate_count[candidate] = counter
        #from shortest to longest string, in case there is a string in the list that is the substring of another strin, remove it
        header_footnotes.sort(key=lambda s: len(s), reverse=True)
        out = []
        for s in header_footnotes:
            if not any([s in o for o in out]):
                out.append(s)
        header_footnotes = out
        #header_footnotes = list(set(header_footnotes) - set(out))

        #count the number of occurences, one candidate can get max 1 count on a slide
        count_dict = {}
        for hf in header_footnotes:
            occurences = 0
            for slide in lecturetext:
                if hf in slide:
                    occurences += 1
            count_dict[hf] = occurences
        #identify the maximum number of occurences of candidates
        #this serves the purpose to prevent false positives
        max_occurence = max(count_dict.values())
        header_footnotes_replace = {}
        for hf in count_dict:
            if  count_dict[hf] >= max_occurence-2:
                header_footnotes_replace[hf] = ""
        return header_footnotes_replace
    except:
        return {}


def remove_footnotes(lecturetext: List, footnotes: Dict) -> List:
    """Remove footnotes from text and return list of text without footnotes"""
    if len(footnotes) < 1:
        return lecturetext
    else:
        index = 0
        for slide in lecturetext:
            for footnote, emptystring in footnotes.items():
                slide = slide.replace(footnote, emptystring)
            lecturetext[index] = slide
            index += 1
        return lecturetext


def remove_url(text: str) -> str:
    """Remove URL"""
    text_no_url = re.sub(r"www\S+|http\S+", " ", text)
    return text_no_url

def remove_punctuation(text: str) -> str:
    """Remove punctuation"""
    text_no_punctuation = re.sub(r"[^a-zA-ZÀ-ž\u0370-\u03FF\u0400-\u04FF\s]+", " ", text)
    return text_no_punctuation

def remove_consecutive_spaces(text: str) -> str:
    """Remove consecutive spaces"""
    text_list = text.split()
    text_no_consecutive_spaces = ' '.join(text_list)
    return text_no_consecutive_spaces


def mark_paragraphs(original_text: str) -> str:
    """Mark paragraphs by adding "~~~" between them"""
    #replace 2 or more new line characters with ~~~
    pragraph_marked = re.sub(r'(?<!\n)\n{2,}(?!\n)', '~~~', original_text)
    #replace new line character followed by non alphabetic character with ~~~
    pragraph_marked = re.sub(r'\n[^A-Za-z]', '~~~', pragraph_marked)
    pragraph_marked = pragraph_marked.lower()
    pragraph_marked = pragraph_marked.replace("\n"," ")
    pragraph_marked = pragraph_marked.split()
    pragraph_marked = ' '.join(pragraph_marked)
    return pragraph_marked



