"""
Author: Konstantinos Lessis
Created: 13.08.2022 
Description: This script contains the function that processes text. It sets the paragraphs attribute
the sentences attribute and the text_for_vectors attribute (cleaned text)

"""

from nturl2path import url2pathname
from .classes.main_class import Lecture
from .helper.textmanagement import get_footnotes, remove_footnotes, remove_consecutive_spaces, remove_punctuation, remove_url, mark_paragraphs
import re



def text_processing(lecture: Lecture) -> Lecture:
    """Set paragraphs attribute
    the sentences attribute and the text_for_vectors attribute"""
    #----set text_for_vector----
    #get lower newline text
    text_lower_newline = lecture.lower_newline_text
    #get footnotes
    lecture.footnotes_replacement_dict = get_footnotes(text_lower_newline)
    #remove footnotes
    text_footnotes_removed = remove_footnotes(text_lower_newline, lecture.footnotes_replacement_dict)
    #remove url
    text_url_removed = [remove_url(slide) for slide in text_footnotes_removed]
    #remove punctuations
    text_punctuation_removed = [remove_punctuation(slide) for slide in text_url_removed]
    #remove consecutive spaces
    text_conspaces_removed = [remove_consecutive_spaces(slide) for slide in text_punctuation_removed]
    lecture.text_for_vector = " ".join(text_conspaces_removed)
    #Add text to slide object of Lecture
    slides = lecture.slides
    #Copy text_for_vector to slides from Lecture object
    slidenumber= 0
    for slide in slides:
        slide.text_for_vector = text_conspaces_removed[slidenumber]
        slidenumber+=1
    
    for slide in slides:
        #----set paragraphs----
        #get original text
        original_text = slide.raw_text
        #replace /n/n with ~~~~
        paragraphs_marked = mark_paragraphs(original_text)
        #lower, remove newline characters
        paragraphs_marked = paragraphs_marked.lower()
        paragraphs_marked = paragraphs_marked.replace("\n"," ")
        paragraphs_marked = paragraphs_marked.split()
        paragraphs_marked = ' '.join(paragraphs_marked) 
        #remove footnotes
        for footnote, emptystring in lecture.footnotes_replacement_dict.items():
            paragraphs_marked = paragraphs_marked.replace(footnote, emptystring)
        #remove url
        paragraphs_marked = remove_url(paragraphs_marked)
        #split into paragraphs
        paragraphs = paragraphs_marked.split("~~~")
        paragraphs = [' '.join(paragraph.split()) for paragraph in paragraphs]
        #creat list with paragraphs that are not empty or only have space
        paragraphs_no_empty = []
        for paragraph in paragraphs:
            if len(paragraph)>0 and paragraph != " ":
                paragraphs_no_empty.append(paragraph)
        
        paragraphs_final = []
        #remove special characters
        for paragraph in paragraphs_no_empty :
            paragraph = re.sub(r"[^a-zA-ZÀ-ž\u0370-\u03FF\u0400-\u04FF\s]+", " ", paragraph)
            if paragraph != " ":
                paragraphs = paragraph.split()
                paragraph = " ".join(paragraphs)
                if len(paragraph)>0:
                    paragraphs_final.append(paragraph)
        #save the paragraphs to the slide object
        slide.paragraphs = paragraphs_final
        #TODO: first paragraph is seen as title, assumes that every page has a title, which is not the case,
        #It could be identified if a page has a title
        #In case slide has no text, there is no paragraph
        try:
            slide.title = paragraphs_final[0]
        except IndexError:
            pass
    
    
    return lecture
