#!/usr/bin/env python3
"""
Parse NCBI Datasets JSON metadata (new schema)
Output: tab-separated file with key fields
"""
import json
import csv
input_file = "Metadata_Col.json"     # input JSON (one object per line)
output_file = "assemblies_metadata_v2_col.tsv"    # output TSV

records = []
with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        data = json.loads(line)

        organism = data.get("organism", {})
        assembly_info = data.get("assembly_info", {})
        assembly_stats = data.get("assembly_stats", {})
        annotation_info = data.get("annotation_info", {})

        biosample = assembly_info.get("biosample", {})

        biosample_attrs = {}
        for attr in biosample.get("attributes", []):
            key = attr.get("name", "").strip().lower().replace(" ", "_")
            val = attr.get("value", "")
            biosample_attrs[key] = val

        record = {
            "accession": data.get("accession", ""),
            "current_accession": data.get("current_accession", ""),
            "paired_accession": data.get("paired_accession", ""),
            "organism_name": organism.get("organism_name", ""),
            "tax_id": organism.get("tax_id", ""),
            "strain": organism.get("infraspecific_names", {}).get("strain", ""),
            "assembly_level": assembly_info.get("assembly_level", ""),
            "assembly_method": assembly_info.get("assembly_method", ""),
            "assembly_status": assembly_info.get("assembly_status", ""),
            "release_date": assembly_info.get("release_date", ""),
            "sequencing_tech": assembly_info.get("sequencing_tech", ""),
            "submitter": assembly_info.get("submitter", ""),
            "gc_percent": assembly_stats.get("gc_percent", ""),
            "total_sequence_length": assembly_stats.get("total_sequence_length", ""),
            "contig_n50": assembly_stats.get("contig_n50", ""),
            "scaffold_n50": assembly_stats.get("scaffold_n50", ""),
            "completeness": data.get("checkm_info", {}).get("completeness", ""),
            "contamination": data.get("checkm_info", {}).get("contamination", ""),
            "bioproject_accession": assembly_info.get("bioproject_accession", ""),
            "biosample_accession": biosample.get("accession", ""),
            "geo_loc_name": biosample.get("geo_loc_name", biosample_attrs.get("geo_loc_name", "")),
            "collection_date": biosample.get("collection_date", biosample_attrs.get("collection_date", "")),
            "isolation_source": biosample.get("isolation_source", biosample_attrs.get("isolation_source", "")),
        }

        record.update(biosample_attrs)

        records.append(record)


all_keys = set()
for r in records:
    all_keys.update(r.keys())
all_keys = sorted(all_keys)

with open(output_file, "w", newline="", encoding="utf-8") as out:
    writer = csv.DictWriter(out, fieldnames=all_keys, delimiter="\t")
    writer.writeheader()
    writer.writerows(records)

print(f"✅ Parsed {len(records)} genome entries")
print(f"📄 Output written to: {output_file}")
print(f"🧬 Total columns: {len(all_keys)}")
