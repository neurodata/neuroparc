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
        help="""The directory where the atlases you wish to analyze are saved.""",
        action="store",
    )
    parser.add_argument(
        "--output_dir",
        help="""Directory to save the output adjacency matrix. If not specified, then
        the input directory will be used. Default is None.""",
        action="store",
        default=None,
    )
    parser.add_argument(
        "--fig_name",
        help = """Name to use for the output png and csv files. If not specified, then
        the name 'AMI_Matrix' will be used. Default is 'AMI_Matrix'""",
        action = "store",
        default = 'AMI_Matrix',
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
        nargs="+",
    )

    # ------- Parse CLI arguments ------- #
    result = parser.parse_args()
    input_dir = result.input_dir
    output_dir=result.output_dir
    fig_name = result.fig_name
    voxel_size = result.voxel_size
    atlases = result.atlas_names
    

    # Save outputs to input directory if output directory not specified
    if not output_dir:
        output_dir=input_dir

    #Search for all applicable files
    if atlases:
        #Append input directory to atlas_names
        atlas_paths = [f"{input_dir}/{i}" for i in atlases]
    else:
        dims = f"{voxel_size}x{voxel_size}x{voxel_size}"
        
        atlas_paths = [
        i for i in glob.glob(input_dir + f"/*{dims}.nii.gz") if dims in i
        ]


    #Create a ndarray of zeros to be filled in
    AMI_array = np.zeros((len(atlas_paths)+1,len(atlas_paths)+1))

    #Loop through all combinations of atlases specified and calculate AMI
    for i in range(len(atlas_paths)):
        for j in range(len(atlas_paths)):
            if i >= j:
                AMI = adjusted_mutual_info(atlas_paths[i],atlas_paths[j])
                AMI_array[int(i)][int(j)]=float(AMI)
                AMI_array[int(j)][int(i)]=float(AMI)

    #Save AMI matrix to csv file, comma delimited
    np.savetxt(f'{output_dir}/{fig_name}.csv', AMI_array, delimiter=",")

    #Generate labels for figure
    for i in range(len(atlases)):
        atlases[i] = atlases[i].split('_space-')[0]

    fig, ax = plt.subplots()
    im = ax.imshow(AMI_array, cmap="gist_heat_r") #Can specify the colorscheme you wish to use
    ax.set_xticks(np.arange(len(atlases)))
    ax.set_yticks(np.arange(len(atlases)))

    ax.set_xticklabels(atlases)
    ax.set_yticklabels(atlases)

    #Label x and y-axis, adjust fontsize as necessary
    plt.setp(ax.get_xticklabels(), fontsize=6, rotation=90, ha="right", va="center", rotation_mode="anchor")
    plt.setp(ax.get_yticklabels(), fontsize=6)

    plt.colorbar(im, aspect=30)
    ax.set_title("Adjusted Mutual Information Between Atlases")
    
    fig.tight_layout()

    plt.show()

    plt.savefig(f'{output_dir}/{fig_name}.png', dpi=1000)



if __name__ == "__main__":
    main()