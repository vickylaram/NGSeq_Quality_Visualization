#!/bin/sh
wget https://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.9.zip && python -m zipfile -e fastqc_v0.11.9.zip ./FastQC/

if ! [ -d ./FastQC ]; then
  mkdir /FastQC
fi

if ! [ -d ./FastQC_Output ]; then
  mkdir /FastQC_Output
fi

if wget -qO- https://get.nextflow.io | bash ; then
    chmod +x ./nextflow
fi

export PIPENV_VENV_IN_PROJECT="enabled" && pipenv install
