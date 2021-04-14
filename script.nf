#!/usr/bin/env nextflow

params.input = "$PWD"
params.output = "$PWD/FastQC_Output"

files = Channel.fromPath(params.input + "/*.fastq.gz")
/*condaEnvYamlFile = "$PWD/environment.yaml"*/


process runFastqc {

    input:
    val file from files

    output:
    stdout into result1

    script:
    """
    if [ -d "$params.input" ]; then
    [[ -d "$params.output" ]] || mkdir "$params.output"
    chmod 755 $PWD/FastQC/fastqc
    $PWD/FastQC/fastqc "$file" -o $params.output --extract
    echo "Processing $file ...."
    else
    echo "Warning: '$params.input' NOT found."
    fi
    """

}


process startDash {

   output:
   stdout into result2

   script:
   """
   python3 $PWD/src/main.py "$params.output"
   """
}
result2.subscribe { println it }
result1.subscribe { println it }
