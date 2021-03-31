#!/usr/bin/env nextflow

params.input = "$PWD"
params.output = "$PWD/FastQC_Output"

files = Channel.fromPath(params.input + "/*.fastq.gz")


process runFastqc {
/*
    fastqc $params.input -o $params.output
    params.input = params.input + "/*.fastq.gz"


    for file in $params.input/*.fastq.gz; do
    echo "$file"
    done
    $PWD/FastQC/fastqc "$file" -o $params.output
    echo "'$params.input' found and now copying files, please wait ..."

    for file in $params.input/*.fastq.gz; do
    echo "$file"
    done

*/

    input:
    val file from files

    output:
    stdout into result


    script:
    """
    if [ -d "$params.input" ]; then
    [[ -d "$params.output" ]] || mkdir "$params.output"
    $PWD/FastQC/fastqc "$file" -o $params.output
    echo "Processing $file ...."
    else
    echo "Warning: '$params.input' NOT found."
    fi

    """

}

result.subscribe { println it }
