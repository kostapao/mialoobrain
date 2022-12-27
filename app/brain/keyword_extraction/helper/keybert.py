"""
Author: Konstantinos Lessis
Created: 19.08.2022 
Description: This script contains the function that checks all pos candidates and sorts them with cosine similarities using the language model BERT

"""

from torch import Tensor
from typing import List
import numpy as np
from numpy import ndarray
from sentence_transformers import SentenceTransformer,util




#Import model
model = SentenceTransformer('all-MiniLM-L6-v2')


def calculate_bert_vector(text: str) -> ndarray:
    embedding = model.encode(text)
    return embedding



def calculate_cosine_similarity(emb1: ndarray, emb2: ndarray) -> Tensor:
    return(util.cos_sim(emb1, emb2))












# # def cosine_distance(vector_a, vector_b): # -> Float
# #     pass