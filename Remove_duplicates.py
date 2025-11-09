"""
Gene Annotation Deduplication Script

This script loads, processes, and deduplicates gene annotation data from a
tab-separated file using pandas.

Deduplication logic:
1. Keep one representative per unique combination of (SEQUENCE, START, END, STRAND)
   — chosen by highest %COVERAGE, then highest %IDENTITY.
2. Then, within the same (GENE, SEQUENCE, STRAND), keep only the entry
   with the highest %COVERAGE and %IDENTITY.

Example usage:
    python Remove_duplicatess.py -i annotations.tsv -o annotations_deduplicated.tsv
"""

import pandas as pd
import argparse


def load_and_deduplicate_annotations(input_file: str, output_file: str):
    # Load the TSV file
    df = pd.read_csv(input_file, sep='\t', dtype=str)

    # Convert numeric columns to float for comparison
    df["%COVERAGE"] = pd.to_numeric(df["%COVERAGE"], errors="coerce")
    df["%IDENTITY"] = pd.to_numeric(df["%IDENTITY"], errors="coerce")

    # -------------------------------
    # Step 1: Deduplicate by genomic coordinates
    # -------------------------------
    df_sorted = df.sort_values(
        by=["SEQUENCE", "START", "END", "STRAND", "%COVERAGE", "%IDENTITY"],
        ascending=[True, True, True, True, False, False]
    )
    df_dedup = df_sorted.drop_duplicates(subset=["SEQUENCE", "START", "END", "STRAND"], keep="first")

    # -------------------------------
    # Step 2: Deduplicate by gene on same SEQUENCE and STRAND
    # -------------------------------
    df_final_sorted = df_dedup.sort_values(
        by=["SEQUENCE", "STRAND", "GENE", "%COVERAGE", "%IDENTITY"],
        ascending=[True, True, True, False, False]
    )
    df_final = df_final_sorted.drop_duplicates(subset=["SEQUENCE", "STRAND", "GENE"], keep="first")

    # -------------------------------
    # Save the output
    # -------------------------------
    df_final.to_csv(output_file, sep="\t", index=False)

    print(f"✅ Deduplicated and filtered data saved to: {output_file}")
    print(f"Rows before: {len(df)}, after step 1: {len(df_dedup)}, after step 2: {len(df_final)}")

    return df_final


def main():
    parser = argparse.ArgumentParser(
        description="Deduplicate and filter gene annotation data based on %COVERAGE and %IDENTITY."
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Input gene annotation TSV file (e.g., annotations.tsv)"
    )
    parser.add_argument(
        "-o", "--output",
        default="annotations_deduplicated.tsv",
        help="Output deduplicated TSV file (default: annotations_deduplicated.tsv)"
    )

    args = parser.parse_args()

    load_and_deduplicate_annotations(args.input, args.output)


if __name__ == "__main__":
    main()
