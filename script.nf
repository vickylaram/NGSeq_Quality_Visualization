#!/usr/bin/env nextflow

params.input = "" + "/*.fastq.gz"
params.output = "$PWD/FastQC_Output"


/*
println "Input: $params.input"
println "Output: $params.output"

*/

process runFastqc {
/*
    fastqc $params.input -o $params.output
    params.input = params.input + "/*.fastq.gz"

    for i in $(ls *.fastq.gz);
    do
    $PWD/FastQC/fastqc $i -o $params.output
    echo "'$params.input' found and now copying files, please wait ..."
    done


*/
    output:
    stdout into result


    script:
    """
    if [ -d "$params.input" ]; then
    [[ -d $params.output ]] || mkdir $params.output




    else
    echo "Warning: '$params.input' NOT found."
    fi

    """

}

result.subscribe { println it }
