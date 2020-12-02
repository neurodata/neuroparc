# Script Descriptions

There are three major programs used in the preperation of a neuroparc repository atlas. Each script has an accompanying Jupyter Notebook file which walks you through an example run.

## json_generation.py
Jupyter Notebook Tutorial: Json_Generation_Tutorial.ipynb\
Takes a parcellation file and aligns it to a desired reference anatomical file. This script will resample the parcellation file to a desired voxel resolution and reorient the file as necessary. This script works best on parcellations that cover the majority of the brain. It will output a json file containing the coordinates of the center of each ROI (based on voxel value), the amount of voxels in each ROI, and the average ROI area. The json file will also contain additional locations to input metadata and source information for the parcellation. Note that the metadata will have to be compleated before it will be accepted into the neuroparc repository.

Inputs:
- Parcellation file (.nii or .nii.gz)
- Reference anatomical brain for the parcellation to be registered too (Several MNI scans can be found in the atlases/reference_brains directory)
- Desired voxel resolution (mm) for parcellation to be resampled too
- [optional] csv containing anatomical labels for each voxel value which will inform the output json file

Outputs:
- json file
- registered parcellation

## dice_correlation.py
Jupyter Notebook Tutorial: Dice_Correlation_Tutorial.ipynb\
Calculates the dice correlation value of for each set of ROIs between two parcellations. These dice values are then saved to a csv file and used to create a heatmap png. If more than two parcellations are provided, the script will itterate through all possible pairs of parcellations, creating the heatmap and csv file for each pair.

Inputs:
- 2+ parcellation files (.nii or .nii.gz)
- output directory

Outputs:
- heatmap png of each combination of atlases
- csv file containing all dice correlation values

## adjusted_mutual.py
Jupyter Notebook Tutorial: Adjusted_Mutual_Tutorial.ipynb\
Calculates the adjusted mutual information (AMI) score between parcellations. If more than 2 parcellations are input, then it will create a heatmap png containing the AMI of each parcellation pair. A csv file is also saved containing the data used for the heatmap. Input parcellations must have same voxel size and orientation for proper results.

Inputs:
- parcellations (if an input directory is given then all eligible parcellations will be used)
- [optional] voxel_size
- [optional] name to use for output files

Outputs:
- heatmap png containing adjusted mutual of each
- csv file containing the AMI for each pair of parcellations
