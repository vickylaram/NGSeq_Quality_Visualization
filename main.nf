#!/usr/bin/env nextflow


params.input = "$PWD/data"
params.output = "$PWD/FastQC_Output/"

files = Channel.fromPath(params.input + "/*.fastq.gz")

envFile = Channel.fromPath("$PWD/environment.yaml")

/*condaEnvYamlFile = "$PWD/environment.yaml"*/


process activateEnv {
    
}

process createOutputDir {
    script:
    """
    if [ -d "$params.input" ]; then
    [[ -d "$params.output" ]] || mkdir "$params.output"
    echo "SUCCESS: '$params.input' created."
    else
    echo "Warning: '$params.input' NOT found."
    fi
    """
}

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
   python3 $PWD/src/main.py "$params.output"
   """
}

/*result2.subscribe { println it }
result1.subscribe { println it }*/
