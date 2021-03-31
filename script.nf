#!/usr/bin/env nextflow

params.input = "$PWD"
params.output = "$PWD/FastQC_Output"

files = Channel.fromPath(params.input + "/*.fastq.gz")
condaEnvYamlFile = "$PWD/environment.yaml"

/*
process setUpCondaEnvironment {

    script:
    """
    conda init zsh
    conda env create -f $condaEnvYamlFile
    conda activate ngseq_quality_visualisation
    """
}
*/
process runFastqc {

    input:
    val file from files

    output:
    stdout into result

    script:
    """
    if [ -d "$params.input" ]; then
    [[ -d "$params.output" ]] || mkdir "$params.output"
    chmod 755 $PWD/FastQC/fastqc
    $PWD/FastQC/fastqc "$file" -o $params.output
    echo "Processing $file ...."
    else
    echo "Warning: '$params.input' NOT found."
    fi
    """

}

result.subscribe { println it }
