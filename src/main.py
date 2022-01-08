import sys
import visualization as v
import io_util as io

if __name__ == '__main__':
    if len(sys.argv) > 1:

        v.fastqc_output_path = str(sys.argv[1])
        v.set_data(io.read_fastqc_data(str(sys.argv[1])))
        #v.__data =

        v.__get_available_files(v.__data)
        v.run_app()
    else:
        print("Please provide path")
        #raise FileNotFoundError
