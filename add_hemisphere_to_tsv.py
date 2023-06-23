from pathlib import Path
from rich import print
import pandas as pd
import json

RENAME = False

root_dir = Path(__file__).parent

output_dir = root_dir / "atlases" / "label" / "Human"

tsv_files = output_dir.glob("*.tsv")

for file in tsv_files:
    df = pd.read_csv(file, sep="\t")
    hemispheres = []
    for row in df.iterrows():
        label = row[1]["label"]
        if label.startswith("L_") or label.startswith("Left_"):
            hemispheres.append("left")
        elif label.startswith("R_") or label.startswith("Right_"):
            hemispheres.append("right")
        else:
            hemispheres.append("bilateral")

    df["hemisphere"] = hemispheres
    
    print(df)

    if RENAME:
        df.to_csv(file, sep="\t", index=False)
