#!/bin/bash

OUTPUT_DIR=./data/filtered

if [ ! -d  $OUTPUT_DIR ]; then 
    mkdir "$OUTPUT_DIR"
fi

{
for file in ./data/*.json; do
    echo Filtering $(basename "$file")
    python filter_data.py $file -o "$OUTPUT_DIR"
done
} >> ./logs/filtering_$(date +%F).log 2>&1