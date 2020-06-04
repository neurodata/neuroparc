import nibabel as nb
import numpy as np
import glob
from matplotlib import pyplot as plt
from sklearn import metrics as skm
from argparse import ArgumentParser


def adjusted_mutual_info(atlas1, atlas2):
    """Calculate adjusted mutual information between two atlases

    Parameters
    ----------
    atlases : [type]
        [description]
    """
    
    at1 = nb.load(atlas1)
    at2 = nb.load(atlas2)

    atlas1 = at1.get_data()
    atlas2 = at2.get_data()

    AMI = skm.adjusted_mutual_info_score(atlas1.flatten(),atlas2.flatten())

    return AMI



def main():
    parser = ArgumentParser(
        description="Script to calculate the adjsted mutual information of atlases"
    )
    parser.add_argument(
        "input_dir",
        help="""The""",
        action="store",
    )
    parser.add_argument(
        "--voxel_size",
        help="""Voxel_size for atlases to be analyzed, this will filter
        the files located in the input_dir file for anything with 
        <atlas_name>_res-<VOX>x<VOX>x<VOX>.nii.gz""",
        action="store",
        default="1",
    )
    parser.add_argument(
        "--atlas_names",
        help="""List of atlas names to analyze, located in the directory
        specified by input_dir. If not specified, then all atlases in the input
        directory will be analyzed. These override the value specified in
        '--voxel_size'. Default is None.""",
        action="store",
        default=None,
    )

    # ------- Parse CLI arguments ------- #
    result = parser.parse_args()
    input_dir = result.input_dir
    voxel_size = result.voxel_size
    atlases = result.atlas_names

    #Search for all applicable files
    if atlases:
        #Append input directory to atlas_names
        atlas_paths = [f"{input_dir}/{i}" for i in atlases]
    else:
        dims = f"{voxel_size}x{voxel_size}x{voxel_size}"
        
        atlas_paths = [
        i for i in glob.glob(input_dir + f"/*{dims}.nii.gz") if dims in i
        ]

    
    #Run through all combinations of atlases and calculate adjusted mutual information
    
    AMI_array = np.zeroes((len(atlas_paths),len(atlas_paths)))

    a=0
    b=0

    for i in atlas_paths:
        for j in atlas_paths:
            AMI = adjusted_mutual_info(i,j)
            AMI_array[int(a)][int(b)]=float(AMI)

            b=b+1
        a=a+1

    #Generate figure



if __name__ == "__main__":
    main()