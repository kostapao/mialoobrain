"""
Author: Konstantinos Lessis
Created: 20.06.2022 
Description: File containing the main classes the whole script works with, Lectures, Slides and Keyxwords
"""


class Lecture():
    def __init__(self):
        self.path = None
        self.name = None
        self.name_pure = None
        self.slides = []
        self.footnotes = None
        self.lecturepdf = None
        #TODO: Wieso kein Array?
        self.footnotes_replacement_dict = None
        #List of slide texts used for BERT language model
        #set in texprocess.py
        self.text_for_vector = None
        self.bert_vector = None
        self.n_gram_count_dict = None
        #wikipedia prep
        self.number_of_similarity_clusters = None
        


    def __str__(self):
        return self.name_pure

    def __repr__(self):
        return self.__str__()

    #When lecture.lower_newline_text is executed, the function below will be run
    @property
    def lower_newline_text(self):
        return [slide.lower_newline for slide in self.slides]

    #When lecture.length is executed, the function below will be run
    @property
    def length(self):
        return len(self.slides)



class Slide():
    def __init__(self):
        self.name = None
        self.name_pure = None
        self.pdf_path = None
        self.img_path = None
        self.pagenum = None
        self.lecture_name_pure = None
        self.image_name = None
        self.raw_text = None
        #set in textmanagement.py
        self.title= None
        #set in texprocess.py
        self.text_for_vector = None
        self.bert_vector = None
        #set in texprocess.py
        self.paragraphs = None
        #set in keywordextraction.py
        self.keywords = None
        self.slidepdf = None
        self.slideimg = None
        #n_grams
        self.tokens = None
        self.bi_grams = None
        self.tri_grams = None
        self.four_grams = None

        

    def __str__(self):
        return self.name_pure

    def __repr__(self):
        return self.__str__()

    @property 
    def lower_newline(self):
        """transform raw text to lower and replace newline character with space"""
        lower_text = self.raw_text.lower()
        newline_a = lower_text.replace("\n"," ")
        newline_b = newline_a.split()
        lower_newline_text = " ".join(newline_b)
        return lower_newline_text







class Keyword():
    def __init__(self,pos,is_in_title):
        self.pos = pos
        self.is_in_title = is_in_title
        #BERT Related
        self.bert_vector = None
        self.is_relevant = False
        self.cos_sim_slide = None
        self.cos_sim_neighbour = None
        self.cos_sim_lecture = None

        #wikipedie prep
        self.lecture_similarity_cluster = None

        #Wikipedia Related
        #self.wiki_url = None #str
        self.wiki_title = None # str
        self.wiki_links = None #{title:link}
        self.wiki_disambiguation = False #bool
        self.wiki_search_results = None #list of tuples because order important
        self.wiki_no_article = False #bool


    def __str__(self):
       return self.pos

    def __repr__(self):
        return self.__str__()

    @property
    def get_wiki_url(self):
        spaces_replaced = self.wiki_title.replace(" ","_")
        return "https://en.wikipedia.org/wiki/" + spaces_replaced
