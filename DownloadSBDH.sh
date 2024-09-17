#!/bin/bash

# Input file containing SBDH IDs and corresponding information
input_file="/home/varshineas/Reference/hg38/hg38_all_dataset_info_table.txt"

# Directory to store downloaded .txt files
output_dir="/home/varshineas/Data/hg38/SBDH/"

# Check if the input file exists and is readable
if [[ ! -f "$input_file" ]]; then
  echo "Error: Input file '$input_file' does not exist or is not a regular file."
  exit 1
fi

if [[ ! -r "$input_file" ]]; then
  echo "Error: Input file '$input_file' is not readable."
  exit 1
fi

# Ensure the output directory exists
mkdir -p "$output_dir"

# Read through the input file and download the SBDH files
# Format of the input file is assumed to be: DataSetId (SBDH), Species, SeqType, GeneSymbol, etc.
tail -n +2 "$input_file" | while IFS=$'\t' read -r DataSetId Species SeqType GeneSymbol CellTissue Treatment Source MainAccession SubAccession FileName_RBP UniqAccession Assembly newFileName CitationForShort Citation PubMedID Title mutation
do
  # Use DataSetId (SBDH ID) as the output filename with .txt extension
  filename="${output_dir}${DataSetId}.txt"

  # Check if the file already exists
  if [[ -f "$filename" ]]; then
    echo "File $filename already exists. Skipping download."
    continue
  fi

  # Download the file using curl
  echo "Downloading $filename..."
  curl -s "https://rnasysu.com/encori/api/bindingSite/?assembly=hg38&datasetID=$DataSetId" -o "$filename"

  # Check if the curl command was successful
  if [[ $? -ne 0 ]]; then
    echo "Error: Failed to download $filename."
  else
    echo "Downloaded $filename successfully."
  fi

done

echo "All downloads complete."
