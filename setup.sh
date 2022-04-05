#!/bin/sh

############################################################
# Help                                                     #
############################################################
Help()
{
   # Display Help
   echo "You can run this script with the following flags, if you need to install any of the needed languages/tools (Java, Python, Pipenv)"
   echo
   echo "Syntax: setup [-j|-py|-pipenv|-h]"
   echo "options"
   echo "h     Print this Help."
   echo "pipenv     Install Pipenv."
   echo
}

Setup()
{

  wget https://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.9.zip && python -m zipfile -e fastqc_v0.11.9.zip ./

  rm -rf fastqc_v0.11.9.zip
  #if ! [ -d ./FastQC ]; then
   #mkdir /FastQC
  #fi

  if ! [ -d ./FastQC_Output ]; then
    mkdir /FastQC_Output
  fi

  if wget -qO- https://get.nextflow.io | bash ; then
      chmod +x ./nextflow
  fi

  export PIPENV_VENV_IN_PROJECT="enabled" && pipenv install
}

#while getopts "hp:" option; do
#   case $option in
#      h) # display Help
#         Help
#         exit;;
#      p)
#         pip3 install pipenv
#         exit;;
#      \?) # Invalid option
#         echo "Error: Invalid option"
#         exit;;
#   esac
#
#done

Setup
