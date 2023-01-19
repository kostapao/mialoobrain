"""
Author: Konstantinos Lessis
Created: 20.06.2022 
Description: File containing classes that represent pdfs and images, they are used for loading the data
"""

import os
from xmlrpc.client import Boolean
#import data_preprocessing.pathvar as pathvar
from ..helper.pathmanagement import pdf_split_subfolder, img_split_subfolder
from PyPDF2 import  PdfFileWriter, PdfFileReader
from pdf2image import convert_from_path
import tika
from PIL import Image
import pytesseract
from typing import List
from .main_class import Lecture, Slide

#TODO: Uncomment for remote
#TODO: Comment for local
os.environ['TIKA_CLIENT_ONLY'] = "1"
os.environ['TIKA_SERVER_ENDPOINT'] = "http://tika:9998"

from tika import parser



class LecturePdf:
    def __init__(self, path) -> None:
        self.path = path
        self.name = path.split("/")[-1]
        #name without filetype ending
        self.name_pure = self.name.split(".")[0]
        #path to store split pdf & images
        self.pdf_split_dir = os.path.join(pdf_split_subfolder,self.name_pure)
        #self.pdf_split_dir = os.path.join(pathvar.pdf_split_subfolder,self.name_pure)
        self.img_split_dir = os.path.join(img_split_subfolder,self.name_pure)
        #self.img_split_dir = os.path.join(pathvar.img_split_subfolder,self.name_pure)
        #TODO: What if 2 files have the same name Option: MD5 Hash in DB with already processed files?
        #when initializing a new lecture, create pdf to save single pdfs and images
        if self.__class__ == LecturePdf:
             self.create_pdf_dir()
             self.create_img_dir()

    def __str__(self) -> None:
        return self.name_pure
    
    def create_pdf_dir(self) -> None:
        """Create directory to save slides as single pdf"""
        if os.path.isdir(self.pdf_split_dir):
            pass
        else:
            os.mkdir(self.pdf_split_dir)
        

    def create_img_dir(self) -> None:
        """Create directory to save slides as images"""
        if os.path.isdir(self.img_split_dir):
            pass
        else:
            os.mkdir(self.img_split_dir)

    def split_to_pdf(self) -> None:
        read_pdf = PdfFileReader(open(self.path, "rb"),False)
        for page in range(read_pdf.numPages):
            output = PdfFileWriter()
            output.addPage(read_pdf.getPage(page))
            pagenum = page+1
            single_pdf_path = self.pdf_split_dir + "/" + self.name_pure + "_%s.pdf" % pagenum
            with open(single_pdf_path, "wb") as outputStream:
                output.write(outputStream)
    
    def get_pdf_slidepath_list(self) -> None:
        slides = os.listdir(self.pdf_split_dir)
        #In casse pdf split has not been executed, run it here
        if slides == []:
            self.split_to_pdf()
        return 

    def is_latex(self) -> Boolean:
        parsed_tika=parser.from_file(self.path)
        text = parsed_tika["content"]
        if "</latexit>" in text:
            return True
        else:
            return False
    


class SlidePdf(LecturePdf):

    def __init__(self, path):
        self.pdf_path = path
        self.name = path.split("/")[-1]
        #name without filetype ending
        self.name_pure = self.name.split(".")[0]
        self.pagenum = int(self.name_pure.split("_")[-1])
        self.lecture_name_pure = "_".join(self.name_pure.split("_")[:-1])
        self.image_name = self.name_pure + ".jpg"
        self.raw_text = None
        
    def __str__(self) -> str:
        return self.name_pure

    def __repr__(self):
        return self.__str__()

    def extract_text(self) -> str:
        parsed_tika=parser.from_file(self.pdf_path)
        text = parsed_tika["content"]
        return text

    def to_image(self) -> None:
        image = convert_from_path(self.pdf_path)
        image[0].save(os.path.join(img_split_subfolder, self.lecture_name_pure, self.image_name), 'JPEG')
        #image[0].save(os.path.join(pathvar.img_split_subfolder, self.lecture_name_pure, self.image_name), 'JPEG')


class SlideImg(SlidePdf):

    def __init__(self,path):
        super().__init__(path)
        self.img_path = path
        self.raw_text = None

    def extract_text(self):
        return pytesseract.image_to_string(self.img_path)


#--------------------------------------------------HELPER FUNCTIONS---------------------------------------------------------------------------------------        

def lecturepdf_to_lecture(lecturepdf: LecturePdf) -> Lecture:
    lecture = Lecture()
    lecture.path = lecturepdf.path
    lecture.name = lecturepdf.name
    lecture.name_pure = lecturepdf.name_pure
    lecture.lecturepdf = lecturepdf
    return lecture


def slidepdf_to_slide(slidepdf: SlidePdf) -> Slide:
    slide = Slide()
    slide.name = slidepdf.name
    slide.name_pure = slidepdf.name_pure
    slide.pdf_path = slidepdf.pdf_path
    slide.pagenum = slidepdf.pagenum
    slide.lecture_name_pure = slidepdf.lecture_name_pure
    slide.image_name = slidepdf.image_name
    slide.raw_text = slidepdf.raw_text
    slide.slidepdf = slidepdf
    return slide

def slideimg_to_slide(slideimg: SlideImg) -> Slide:
    slide = Slide()
    slide.name = slideimg.name
    slide.name_pure = slideimg.name_pure
    slide.img_path = slideimg.pdf_path
    slide.pagenum = slideimg.pagenum
    slide.lecture_name_pure = slideimg.lecture_name_pure
    slide.raw_text = slideimg.raw_text
    slide.slidepdf = slideimg
    return slide







