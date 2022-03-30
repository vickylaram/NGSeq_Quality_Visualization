import os

import fastqcparser
import pandas as pd
from fastqcparser import FastQCParser

# FastQC raw data is stored in [FOLDER_NAME]/fastq_data.txt
# FOLDER_NAME is the same as the input file used for FastQC analyses
fastqc_data_file = '/fastqc_data.txt'

# Dictionary that contains all file/folder names as keys and their corresponding modules in a list
# as the values of the dict
__dictOfDfs = {}


def get_available_files(data: list[str]) -> dict[str, str]:
    """Function that gets all file names from parsed data
    and creates dictionary for the HTML dropdown selections

    :param data: list of file names as keys (values are not relevant at this point)
    :return: dict with label (which will be presented to the user) and value (used for
    internal purpose only) - in this case they're identical
    """
    available_files = []
    for entry in data:
        available_files.append({'label': entry, 'value': entry})
    return available_files


def read_fastqc_data(fastqc_output_path: str) -> dict[str, list[pd.DataFrame]]:
    """Function that gets FastQC raw output data from directory (from it's subfolders)

    :param fastqc_output_path: absolute path containing FastQC reports in their subfolders
    :return: dict of data of one file
    """

    if fastqc_output_path is not None:
        subfolders_list = __get_extracted_subfolders(fastqc_output_path)
        for subfolder in subfolders_list:
            path = fastqc_output_path + subfolder + fastqc_data_file
            raw_input_data = FastQCParser(path)
            __convert_to_dfs(raw_input_data, subfolder)
        return __dictOfDfs


def __get_extracted_subfolders(fastqc_output_path: str) -> list[str]:
    """Helper function that lists all subfolders of given directory

    :param fastqc_output_path: path to directory where FastQC results are written into
    :return: list of all subfolders of the provided path
    """
    if fastqc_output_path is not None:
        return [d for d in os.listdir(fastqc_output_path) if os.path.isdir(os.path.join(fastqc_output_path, d))]


def __convert_to_dfs(raw_input_data: fastqcparser.FastQCParser, subfolder: str):
    """Helper method that converts the parsed FastQC data
    into Pandas DataFrames for easier plotting later on.
    One file's modules/analyses are converted and added to a list,
    which is later used as the value for the key in __dictOfDfs.

    :param raw_input_data: raw, already Fastqcparser-processed data of one file/subfolder
    :param subfolder: name of file/subfolder being processed, later used as key in dict
    """
    __listOfDfs = []
    for module in raw_input_data.modules.keys():
        module_df = pd.DataFrame(raw_input_data.modules[module]['data'], columns=raw_input_data[module]['fieldnames'])
        __listOfDfs.append(module_df)
    __dictOfDfs[subfolder] = __listOfDfs
