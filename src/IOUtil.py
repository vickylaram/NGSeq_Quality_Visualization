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

def __extractFiles():
    os.chdir(fastqc_output_path)
    for file in glob.glob("*.zip"):
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall()

def __getExtractedSubfolders():
    return [d for d in os.listdir(fastqc_output_path) if os.path.isdir(os.path.join(fastqc_output_path, d))]

def readFastQCDataFile():
    __extractFiles()
    listOfSubfolders = __getExtractedSubfolders()
    for subfolder in listOfSubfolders:
        path = fastqc_output_path + subfolder + fastqc_data_file
        rawInputData = FastQCParser(path)
        parseDataToDf(rawInputData, subfolder)
    return __dictOfDfs

def parseDataToDf(rawInputData, subfolder):
    __listOfDfs = []
    for module in rawInputData.modules.keys():
        module_df = pd.DataFrame(rawInputData.modules[module]['data'], columns=rawInputData[module]['fieldnames'])
        __listOfDfs.append(module_df)
    __dictOfDfs[subfolder] = __listOfDfs
