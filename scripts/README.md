# Script Descriptions

There are three major programs used in the creation of an atlas. Each script has an accompanying Jupyter Notebook file which walks you through and example run. [TODO: Provide example data to run?]

## json_generation.py
Takes a parcellation file and aligns it to a desired reference anatomical file. This script will resample the parcellation file to a desired voxel resolution and reorient the file as necessary. This script works best on parcellations that cover the majority of the brain. It will output a json file containing the coordinates of the center of each ROI (based on voxel value), the amount of voxels in each ROI, and the average ROI area. The json file will also contain additional locations to input metadata and source information for the parcellation. Note that this information will have to be compleated before it will be accepted into the neuroparc repository.

inputs:
- Parcellation file (.nii or .nii.gz)
- Reference anatomical brain for the parcellation to be registered too
- Desired voxel resolution (mm) for parcellation to be resampled too
- [optional] csv containing labels for each voxel value

outputs:
- json file
- registered parcellation

## dice_correlation.py
Calculates dice correlation of multiple parcellations

inputs:
- 2+ parcellation files (.nii or .nii.gz)
- output directory

outputs:
- heatmap png of each combination of atlases

## adjusted_mutual.py
Calculates

inputs:
- parcellations (can use all in a given input directory)
- [optional] voxel_size
- [optional] figure_name

outputs:
- heatmap png containing adjusted mutual of each 
