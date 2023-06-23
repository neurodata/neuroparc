from pathlib import Path
from rich import print
import pandas as pd
import json

RENAME = True

root_dir = Path(__file__).parent

output_dir = root_dir / "atlases" / "label" / "Human"

json_files = output_dir.glob("*.json")

for file in json_files:

    print(file)

    resolution = [x.split("-")[1] for x in file.stem.split("_") if x.startswith("res")][0]

    with open(file) as f:
        content = json.load(f)

    for key in content["MetaData"]:
        if key == "AtlasName":
            new_key = "Name"
        if key == "Source":
            new_key = "ReferencesAndLinks"
        else:
            new_key = "".join([x.capitalize() for x in key.split(" ")])

        if new_key == "ReferencesAndLinks":
            content[new_key] = [content["MetaData"][key]]

        content[new_key] = content["MetaData"][key]
    
    content["Space"] = "MNI152NLin6"
    content["BIDSVersion"] = "1.8.0"
    content["Authors"] = ["", ""]
    content["Species"] = "Homo sapiens"
    content["Resolution"] = f"[{resolution}, {resolution}, {resolution}] mm"

    print(content)