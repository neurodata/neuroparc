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
    with open(file) as f:
        json_content = json.load(f)
