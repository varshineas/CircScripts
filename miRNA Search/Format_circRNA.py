# Input and output files
circular_rna_file = "/home/varshineas/Reference/hg38/human_sequence_v3.0"
output_utr_file = "/home/varshineas/Reference/hg38/circularRNA_UTR.txt"

# Process circular RNA sequences
with open(circular_rna_file, "r") as infile, open(output_utr_file, "w") as outfile:
    for line in infile:
        parts = line.strip().split()
        if len(parts) == 2:
            gene_id = parts[0]
            sequence = parts[1]
            species_id = "9606"  # Human species ID
            outfile.write(f"{gene_id}\t{species_id}\t{sequence}\n")

print(f"Circular RNA UTR input file created at: {output_utr_file}")
