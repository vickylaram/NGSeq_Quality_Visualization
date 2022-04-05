#!/bin/sh

Help(){

  echo "-------- Help --------"
  echo "You can run this script with the following flags, if you need to install any of the needed languages/tools (Java, Python, Pipenv)"
  echo
  echo "Syntax: run [-h|-i (FILE PATH)]"
  echo "options"
  echo "h     Print this Help."
  echo "i     Path to Fastq File(s)"
  echo "----------------------"


}




while getopts "i:" flag;
   do
     case $flag in
       i)
         source .venv/bin/activate
         ./nextflow main.nf --input $OPTARG
         exit;;
       h)
         Help
         exit;;
      \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac

done
