library(Biostrings)

# Set working directory to the location of SBDH files
setwd('/home/varshineas/Data/hg38/SBDH/')

# Read the dataset file
dataset <- read.delim('/home/varshineas/Reference/hg38/hg38_all_dataset_info_table.txt', stringsAsFactors = FALSE, sep = "\t")

# Check the column names to ensure DataSetId exists
print(colnames(dataset))  # Ensure "DataSetId" is a valid column

# Get unique gene symbols from the dataset
genes <- unique(dataset$GeneSymbol)

# Output directory for BED files
output_dir <- '/home/varshineas/Data/hg38/BED/'

# Loop through each gene
for (gene in genes) {
  
  print(paste("Processing gene:", gene))
  
  # Get dataset IDs corresponding to the current gene
  idx <- which(dataset$GeneSymbol == gene)
  
  # Debug: Check which dataset IDs are being selected
  print(paste("Found dataset IDs for gene:", gene, dataset$DataSetId[idx]))
  
  # If no dataset IDs are found for this gene, skip
  if (length(idx) == 0) {
    print(paste("No dataset found for gene:", gene))
    next
  }
  
  datasetnames <- paste(dataset$DataSetId[idx], '.txt', sep = '')
  
  # Debug: Print out the constructed file names to verify correctness
  print(paste("Constructed file paths:", datasetnames))
  
  new_dat <- NULL  # Initialize the data variable
  
  # Loop through each SBDH file for the gene
  for (i in 1:length(datasetnames)) {
    
    file_path <- datasetnames[i]
    
    # Check if the file exists and can be opened
    if (!file.exists(file_path)) {
      print(paste("File does not exist. Skipping:", file_path))
      next
    }
    
    # Try reading the file, skip if there are issues
    tryCatch({
      dat <- read.delim(file_path, skip = 2, header = FALSE)  # Skip only the first 2 lines
      
      # For the first file, initialize new_dat, for subsequent files, append the data
      if (is.null(new_dat)) {
        new_dat <- dat
      } else {
        new_dat <- rbind(new_dat, dat)
      }
    }, error = function(e) {
      print(paste("Error reading file. Skipping:", file_path))
      next
    })
    
  }
  
  # Skip the rest of the loop if no data was successfully read
  if (is.null(new_dat)) {
    print(paste("No valid data found for gene:", gene))
    next
  }
  
  # Remove duplicated rows from new_dat
  new_dat <- new_dat[!duplicated(new_dat), ]
  
  # Write the BED file to the specified directory
  filename <- paste(output_dir, gene, '.bed', sep = '')
  write.table(new_dat, filename, sep = '\t', row.names = FALSE, col.names = FALSE, quote = FALSE)
  
  print(paste("Successfully wrote BED file for gene:", gene, "to", filename))
}
