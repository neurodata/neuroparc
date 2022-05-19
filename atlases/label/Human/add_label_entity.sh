#! /usr/bin/bash

files=$(find ${PWD} -type f -name "*.nii.gz")

echo $files

for i in ${files}; do

    base=$(basename ${i})
    echo ${PWD}/atlas-${base}

    mv ${i} ${PWD}/atlas-${base}

done
