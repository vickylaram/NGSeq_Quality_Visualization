import visualization as v

import os
import sys

if __name__ == '__main__':
    #t = "/Users/vicky/Documents/NGSeq_Quality_Visualization/src"

    #print('Number of arguments:', len(sys.argv), 'arguments.')
    #print ('Argument List:', str(sys.argv))
    '''
    try:
        
    except AssertionError as error:
        print(error)
    else:
        print('Executing the else clause.')


    if len(sys.argv) > 1:
        v.fastqc_output_path = str(sys.argv[1])
        os.path.abspath(os.getcwd())
        
    else:
        print("Please provide path")
        #raise FileNotFoundError
'''
    v.run_app()
