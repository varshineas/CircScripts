import pandas as pd

# File paths
mir_family_file = "/home/varshineas/Reference/hg38/miR_Family.Info.txt"
cross_ref_file = "/home/varshineas/Reference/hg38/hg38_all_miRNA.txt"
output_mirna_file = "/home/varshineas/Reference/hg38/miRNA_input.txt"

# Load files
mir_family_df = pd.read_csv(mir_family_file, sep="\t", usecols=["miR family", "Seed+m8", "Species ID", "MiRBase ID"])
cross_ref_df = pd.read_csv(cross_ref_file, sep="\t", header=None, names=["MiRBase Accession", "Mature miRNA"])

# Filter human miRNAs
human_mirnas = mir_family_df[mir_family_df["Species ID"] == 9606]

# Merge with cross-reference to get mature miRNA IDs
merged_df = pd.merge(human_mirnas, cross_ref_df, left_on="MiRBase ID", right_on="MiRBase Accession", how="inner")

# Create final miRNA input format
merged_df = merged_df[["Mature miRNA", "Seed+m8", "Species ID"]]
merged_df.columns = ["miRNA_family_ID", "seed_region", "species_ID"]

# Save to file
merged_df.to_csv(output_mirna_file, sep="\t", index=False, header=False)
print(f"miRNA input file created at: {output_mirna_file}")
