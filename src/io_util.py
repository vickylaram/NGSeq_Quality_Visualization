import os
import glob
import zipfile
import pandas as pd

import fastqcparser
from pprint import pprint
from fastqcparser import FastQCParser

data_path = '/Users/vicky/Documents/RKI/trainings_data'
fastqc_output_path = '/Users/vicky/Documents/RKI/FastQC_Output/'
fastqc_data_file = '/fastqc_data.txt'

__dictOfDfs = {}


def __extract_files():
    os.chdir(fastqc_output_path)
    for file in glob.glob("*.zip"):
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall()


def __get_extracted_subfolders():
    return [d for d in os.listdir(fastqc_output_path) if os.path.isdir(os.path.join(fastqc_output_path, d))]


def read_fastqc_data():
    __extract_files()
    subfolders_list = __get_extracted_subfolders()
    for subfolder in subfolders_list:
        path = fastqc_output_path + subfolder + fastqc_data_file
        raw_input_data = FastQCParser(path)
        parse_data(raw_input_data, subfolder)
    return __dictOfDfs


def parse_data(raw_input_data, subfolder):
    __listOfDfs = []
    for module in raw_input_data.modules.keys():
        module_df = pd.DataFrame(raw_input_data.modules[module]['data'], columns=raw_input_data[module]['fieldnames'])
        __listOfDfs.append(module_df)
    __dictOfDfs[subfolder] = __listOfDfs
