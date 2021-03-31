import visualization as v
import io_util as io

# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    fastqc_output_path = '/Users/vicky/Documents/NGSeq_Quality_Visualization/FastQC_Output/'
    dict_of_dfs = io.read_fastqc_data(fastqc_output_path)


    print(dict_of_dfs.keys())
    #print(dictOfDfs['190925_19-08244_634-17_S189_L000_R1_001_fastqc'])
    v.run_app(dict_of_dfs)
