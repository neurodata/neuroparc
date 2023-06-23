from pathlib import Path
from rich import print
import pandas as pd

RENAME = False

root_dir = Path(__file__).parent

output_dir = root_dir / "atlases" / "label" / "Human"

def rename_json():

    json_files = (output_dir / "Metadata-json").glob("*.json")

    for file in json_files: 

        filename = file.name

        atlas_name = filename.split("_")[0].split("-")
        atlas_name = camel_case_atlas_name(atlas_name)

        other_entities = "_".join(file.stem.split("_")[1:])

        other_entities = simplify_res(other_entities)

        other_entities = rm_all_label_in_filename(other_entities)

        desc = return_desc_entity(filename)

        new_filename = f"atlas-{atlas_name}_{other_entities}{desc}_dseg.json"

        print(f"{filename} -> {new_filename}")

        if RENAME:
            file.rename(output_dir / new_filename)

def rename_nii():
    nii_files = (output_dir).glob("*.nii.gz")
    for file in nii_files: 

        filename = file.name.replace("_dseg.nii.gz", "")

        atlas_name = filename.split("_")[0].split("-")[1:]
        atlas_name = camel_case_atlas_name(atlas_name)

        other_entities = "_".join(filename.split("_")[1:])

        other_entities = simplify_res(other_entities)

        other_entities = rm_all_label_in_filename(other_entities)

        desc = return_desc_entity(filename)

        new_filename = f"atlas-{atlas_name}_{other_entities}{desc}_dseg.nii.gz"

        if filename != new_filename:
            print(f"{filename}_dseg.nii.gz -> {new_filename}")

            if RENAME:
                file.rename(output_dir / new_filename)

def return_desc_entity(filename):
    desc_label = ""
    if "liberal" in filename:
        desc_label += "liberal"

    if "label_all" in filename:
        desc_label = "labelAll"

    desc = f"_desc-{desc_label}" if desc_label else ""
    return desc

def camel_case_atlas_name(atlas_name):
    if len(atlas_name) > 1:
        atlas_name = "".join([x.capitalize() for x in atlas_name if x != "liberal"])
    else:
        atlas_name = atlas_name[0]
    return atlas_name


def rename_csv():

    csv_files = (output_dir / "Anatomical-labels-csv").glob("*.csv")
    for file in csv_files: 

        desc = return_desc_entity(file.stem)

        filename = file.stem.split("-")
        filename = camel_case_atlas_name(filename)

        df = pd.read_csv(file, names=["index", "label"])
        df = df.dropna()
        print(df)

        new_filename = f"atlas-{filename}{desc}_dseg.tsv"

        if filename != new_filename:
            print(f"{filename}.csv -> {new_filename}")
            if RENAME:
                df.to_csv(output_dir / new_filename, sep="\t", index=False)
                file.unlink()



def simplify_res(filename):
    if "res-1x1x1" in filename:
        filename = filename.replace("res-1x1x1", "res-1")
    if "res-2x2x2" in filename:
        filename = filename.replace("res-2x2x2", "res-2")
    if "res-4x4x4" in filename:
        filename = filename.replace("res-4x4x4", "res-4")
    return filename

def rm_all_label_in_filename(filename):
    if "label_all" in filename:
        filename = filename.replace("_label_all", "")
    return filename


def main():
    rename_json()
    rename_nii()
    rename_csv()

if __name__ == "__main__":
    main()  