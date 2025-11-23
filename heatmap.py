import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np
from matplotlib.patches import Patch

"""
Figura con barras de metadatos
Origen = Study, Type Material, Colombia
Especie = K. pneumoniae, K. variicola, K. quasipneumoniae, etc.
"""
# -------------------------------------------------------------------
# 1️⃣ Load and preprocess
# -------------------------------------------------------------------
input_file = "NEW_Anex_2.txt"
output_dir = "Final_only_heatmap3"
os.makedirs(output_dir, exist_ok=True)

# Load
df = pd.read_csv(input_file, sep="\t")

# Keep metadata
metadata_cols = ["Origen", "Specie identified"]
meta_df = df[["Accession"] + metadata_cols].rename(columns={"Accession": "Genome"})
meta_df.set_index("Genome", inplace=True)

# Drop metadata for heatmap matrix
df.drop(columns=["Origen", "City_Country", "Enviroment/Host", "Isolation Source",
                 "Collection Date", "ID", "Specie identified"], errors='ignore', inplace=True)

# Set genome index
df.rename(columns={"Accession": "Genome"}, inplace=True)
df.set_index("Genome", inplace=True)

# Convert presence (numbers) to 1, '.' to 0
matrix = df.replace('.', 0)
matrix = matrix.apply(pd.to_numeric, errors='coerce').fillna(0)
matrix = (matrix > 0).astype(int)

print("Processed presence/absence matrix:", matrix.shape)

# -------------------------------------------------------------------
# 2️⃣ Define metadata color palettes
# -------------------------------------------------------------------
# Palette for Origin
origin_palette = {
    "Study": "#E1F71C",       # Blue
    "Type Material": "#2F29EB",        # Orange
    "Colombia": "#DC5224"          # Green
}

# Create unique color palette for species (many categories)
species_list = sorted(meta_df["Specie identified"].dropna().unique())
species_palette = sns.color_palette("tab20", n_colors=len(species_list))
species_color_map = dict(zip(species_list, species_palette))

# -------------------------------------------------------------------
# 3️⃣ Create color annotations DataFrame
# -------------------------------------------------------------------
col_colors = pd.DataFrame({
    "Origin": meta_df["Origen"].map(origin_palette),
    "Species": meta_df["Specie identified"].map(species_color_map)
}, index=meta_df.index)

# -------------------------------------------------------------------
# 4️⃣ Generate clustered heatmap with metadata bars
# -------------------------------------------------------------------
sns.set_theme(style="white", context="paper")

cmap = sns.color_palette(["#FEFEFE", "#67E3EC"])

# --- FIX: Avoid duplicate "cbar" keyword by wrapping call safely ---
try:
    g = sns.clustermap(
        matrix,
        cmap=cmap,
        linewidths=0.2,
        linecolor="white",
        cbar_pos=None,           # use cbar_pos instead of cbar keyword
        col_cluster=False,       # disable column clustering -> hide column dendrogram
        row_cluster=False,       # disable row clustering -> hide row dendrogram
        row_colors=col_colors,   # Add side metadata colors
        figsize=(8, 12)
    )

except TypeError:
    # fallback for older seaborn versions (no dendrogram_ratio or cbar_pos)
    g = sns.clustermap(
        matrix,
        cmap=cmap,
        linewidths=0.2,
        linecolor="gray",
        cbar=False,
        col_cluster=False,
        row_cluster=False,
        row_colors=col_colors,
        figsize=(8, 12)
    )
# -------------------------------------------------------------------
# 5️⃣ Customize legends
# -------------------------------------------------------------------
# Build custom patches
origin_patches = [Patch(color=c, label=lab) for lab, c in origin_palette.items()]
species_patches = [Patch(color=c, label=lab) for lab, c in species_color_map.items()]

# Add legends manually to figure
legend1 = plt.legend(handles=origin_patches, title="Origen",
                     loc="lower center", bbox_to_anchor=(0.075, 1.05), frameon=False)
legend2 = plt.legend(handles=species_patches, title="Species",
                     loc="upper right", bbox_to_anchor=(1.25, 1.2), frameon=False, ncol=2, fontsize=6)
plt.gca().add_artist(legend1)

# -------------------------------------------------------------------
# 6️⃣ Save high-resolution figures
# -------------------------------------------------------------------
#g.fig.suptitle("Presence/Absence of Resistance Genes with Metadata", fontsize=14, fontweight="bold")
# Smaller fonts for dense labels
plt.xticks(rotation=45, fontsize=8)
plt.yticks(
    ticks=np.arange(matrix.shape[0]) + 0.5,
    labels=matrix.index,
    rotation=0,
    fontsize=5,      # smaller font for 72 genomes
)
plt.savefig(os.path.join(output_dir, "heatmap_metadata_3.pdf"), bbox_inches="tight", dpi=600)
plt.savefig(os.path.join(output_dir, "heatmap_metadata_3.png"), bbox_inches="tight", dpi=600)
plt.show()
plt.close()

print(f"✅ Heatmap with metadata saved to: {output_dir}")
