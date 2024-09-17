import re

# Paths to input files
bed_file = "/home/varshineas/Reference/hg38/hg38_circRNA_coordinates.bed"
genome_fasta = "/home/varshineas/Reference/hg38/Homo_sapiens.GRCh38.dna.primary_assembly.fa"
output_fasta = "/home/varshineas/Reference/hg38/human_hg38_circRNAs_putative_spliced_sequence.fa"

# Function to parse the genome FASTA file into a dictionary (chromosome -> sequence)
def parse_genome_fasta(genome_fasta):
    sequences = {}
    current_chrom = None
    seq_lines = []
    
    with open(genome_fasta, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if current_chrom:
                    sequences[current_chrom] = ''.join(seq_lines).upper()  # Store chromosome sequence in uppercase
                # Parse the chromosome name from the FASTA header
                current_chrom = line.split()[0][1:]  # Extract chromosome name (after >)
                seq_lines = []
            else:
                seq_lines.append(line)
        
        # Add the last chromosome
        if current_chrom:
            sequences[current_chrom] = ''.join(seq_lines).upper()
    
    return sequences

# Function to extract spliced circular RNA sequence
def extract_circular_rna(bed_line, sequences):
    # Split the line into fields
    fields = bed_line.strip().split()

    # Ensure the BED file has enough fields (check if it has at least 12 fields)
    if len(fields) < 12:
        print(f"Warning: Skipping malformed line: {bed_line}")
        return None
    
    # Extract relevant BED fields
    chrom = fields[0]  # Chromosome
    chrom_start = int(fields[1])  # Start position (global start for the first exon)
    chrom_end = int(fields[2])  # End position (global end for the last exon)
    circ_name = fields[3]  # Circular RNA name
    strand = fields[5]  # Strand
    blockCount = int(fields[9])  # Number of blocks (exons)
    blockSizes = fields[10].strip(',')  # Sizes of the blocks (removes trailing commas)
    blockStarts = fields[11].strip(',')  # Start positions of the blocks relative to chrom_start

    # Split blockSizes and blockStarts into arrays and filter out empty values
    sizes = [int(size) for size in blockSizes.split(',') if size]
    starts = [int(start) for start in blockStarts.split(',') if start]

    # Ensure that sizes and starts match the number of blocks
    if len(sizes) != blockCount or len(starts) != blockCount:
        print(f"Warning: Block count mismatch in {circ_name}. Skipping.")
        return None

    # Check if the chromosome is in the genome sequences
    if chrom not in sequences:
        print(f"Warning: Chromosome {chrom} not found in genome file.")
        return None

    chrom_seq = sequences[chrom]  # Get the full chromosome sequence

    # Extract exons based on the exon sizes and starts relative to the chrom_start
    exon_seqs = []
    for size, start in zip(sizes, starts):
        exon_start = chrom_start + start
        exon_end = exon_start + size
        exon_seq = chrom_seq[exon_start:exon_end]  # Extract exon sequence from the chromosome
        exon_seqs.append(exon_seq)

    # Concatenate the exon sequences
    spliced_seq = ''.join(exon_seqs)

    # If on the reverse strand, reverse complement the sequence
    if strand == '-':
        spliced_seq = reverse_complement(spliced_seq)
    
    return spliced_seq

# Function to get the reverse complement of a DNA sequence
def reverse_complement(seq):
    complement = str.maketrans("ACGT", "TGCA")
    return seq.translate(complement)[::-1]

# Main script
def main():
    # Parse the genome sequences from the FASTA file
    genome_sequences = parse_genome_fasta(genome_fasta)
    
    # Open the output FASTA file
    with open(output_fasta, 'w') as out_fasta:
        # Read the BED file line by line
        with open(bed_file, 'r') as bed:
            for bed_line in bed:
                circ_name = bed_line.split()[3]
                spliced_seq = extract_circular_rna(bed_line, genome_sequences)
                if spliced_seq:
                    out_fasta.write(f">{circ_name}\n")
                    out_fasta.write(f"{spliced_seq}\n")
    
    print(f"Putative spliced circular RNA sequences saved to {output_fasta}")

if __name__ == "__main__":
    main()
