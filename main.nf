#!/usr/bin/env nextflow


params.input = "$PWD/data"
params.output = "$PWD/FastQC_Output/"

files = Channel.fromPath(params.input + "/*.fastq.gz")

process runFastqc {

    input:
    val file from files

    output:
    stdout into result1

    script:
    """
    chmod 755 $PWD/FastQC/fastqc
    $PWD/FastQC/fastqc "$file" -o $params.output --extract
    echo "Processing $file ...."
    """

}

process startDash {

   output:
   stdout into result2

   script:
   """
   python3 $PWD/src/ngs_visualization.py "$params.output"
   """
}

