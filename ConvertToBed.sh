awk 'NR>1 {print $1 "\t" $2 "\t" $3 "\t" $5 "\t" "." "\t" $4}' /home/varshineas/Reference/hg38/hg38_circRNA_circAtlasv3.0.txt > /home/varshineas/Reference/hg38/hg38_circRNA_circAtlasv3.0.bed
