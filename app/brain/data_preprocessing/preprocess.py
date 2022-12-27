"""
Author: Konstantinos Lessis
Created: 20.06.2022 
Description: This script processes a pdf file by spliting it and extracting text,
in case direct pdf extraction fails, ocr is done by transforming the slides to images first

"""

from re import A
from .classes.main_class import Slide, Lecture
from .classes.load_class import LecturePdf, SlidePdf, SlideImg,lecturepdf_to_lecture, slidepdf_to_slide, slideimg_to_slide
import os
from typing import List
from .helper.pathmanagement import get_dir_filepaths,delete_dir_content,raw_data




def data_preprocessing(path: str) -> Lecture:
    """
    Split pdf to single pdfs and then return text in form of """
    #Read File
    lecture_pdf = LecturePdf(path)
    lecture = lecturepdf_to_lecture(lecture_pdf)

    #Split PDF and save single pdfs
    lecture_pdf.split_to_pdf()

    #Extract text from slides and create dictionary with all files
    lecture_slides = []
    if lecture_pdf.is_latex() == False:
        pdf_slide_paths = get_dir_filepaths(lecture_pdf.pdf_split_dir)
        for pdf_slide_path in pdf_slide_paths:
            #pdf_slide_path = os.path.join(lecture_pdf.pdf_split_dir,pdf_slide_name)
            #print(pdf_slide_path)
            slide = SlidePdf(pdf_slide_path)
            slide_text = slide.extract_text()
            #Set text attribute to extracted text
            slide.raw_text = slide_text
            #slidepdf to slide
            slide = slidepdf_to_slide(slide)
            lecture_slides.append(slide)
        #Add slides to lecture instance
        lecture.slides = lecture_slides
            #delete all files and folder
        delete_dir_content(lecture_pdf.pdf_split_dir,including_dir = True)
        
        #get folder where original file
        #full_path = lecture.path.split("/")[:-1].join("/")

        delete_dir_content(lecture_pdf.img_split_dir,including_dir = True)
        delete_dir_content(raw_data)
        return lecture

    else:
        #TODO: Could we recognize latex tags and remove them? Instead of image transformation
        #Transform every PDF to image and save in img_split directory
        pdf_slide_paths = get_dir_filepaths(lecture_pdf.pdf_split_dir)
        for pdf_slide_path in pdf_slide_paths:
            slide = SlidePdf(pdf_slide_path)
            slide.to_image()
        #Extract text from every image
        img_slide_paths = get_dir_filepaths(lecture_pdf.img_split_dir)
        for img_slide_path in img_slide_paths:
            slide = SlideImg(img_slide_path)
            slide_text = slide.extract_text()
            #Set text attribute to extracted text
            slide.raw_text = slide_text
            #slidepdf to slide
            slide = slideimg_to_slide(slide)
            lecture_slides.append(slide)
        #Add slides to lecture instance
        lecture.slides = lecture_slides
        delete_dir_content(lecture_pdf.pdf_split_dir,including_dir = True)
        
        #get folder where original file
        #full_path = lecture.path.split("/")[:-1].join("/")

        delete_dir_content(lecture_pdf.img_split_dir,including_dir = True)
        delete_dir_content(raw_data)
        return lecture       
