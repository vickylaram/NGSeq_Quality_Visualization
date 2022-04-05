#!/bin/sh

############################################################
# Help                                                     #
############################################################
Help()
{
   echo "-------- Help --------"
   echo "You can run this script with the following flags, if you need to install any of the needed languages/tools (Java, Python, Pipenv)"
   echo
   echo "Syntax: setup [-pipenv|-h]"
   echo "options"
   echo "h     Print this Help."
   echo "p     Install Pipenv."
   echo "----------------------"
}

Setup()
{

  echo "-------- Setting env up --------"

  echo "-------- Downloading and extracting FastQC --------"
  wget https://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.9.zip && python -m zipfile -e fastqc_v0.11.9.zip ./

  rm -rf fastqc_v0.11.9.zip

  echo "-------- Downloading Nextflow --------"
  if wget -qO- https://get.nextflow.io | bash ; then
      chmod +x ./nextflow
  fi

  echo "-------- Creating output directory --------"
  if ! [ -d ./FastQC_Output ]; then
    mkdir ./FastQC_Output
  fi

  echo "-------- Setting up pipenv environment --------"

  export PIPENV_VENV_IN_PROJECT="enabled" && pipenv install


  echo "-------- Setup finished successfully! --------"
  echo "----------------------"
}


while getopts "hp" option; do
   case $option in
      h) # display Help
         Help
         exit;;
      p)
         echo "-------- Installing pipenv --------"
         pip3 install pipenv;;
      \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac

done

Setup
