"""
Author: Konstantinos Lessis
Created: 20.06.2022 
Description: File containing variables with path values that are regularly used
"""

import os
from natsort import natsorted, ns
from typing import List
import shutil

#Current Directory
current_dir = os.getcwd()

#Data Engineering Paths
raw_data = os.path.join(current_dir,"app/brain/data")
pdf_split_subfolder = os.path.join(current_dir,"app/brain/data_preprocessing/split/pdf_split")
img_split_subfolder = os.path.join(current_dir,"app/brain/data_preprocessing/split/img_split")


def get_dir_filepaths(dir_path: str) -> List[str]:
    """Return absolute file paths from files in dir_path in alist"""
    file_paths = [os.path.join(dir_path,file) for file in os.listdir(dir_path) if file[0] != "."]
    return natsorted(file_paths, alg=ns.IGNORECASE)


def delete_dir_content(path: str, including_dir = False):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    if including_dir:
        os.rmdir(path)