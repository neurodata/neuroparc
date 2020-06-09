import nibabel as nb
import numpy as np
from argparse import ArgumentParser
import matplotlib
from matplotlib import pyplot as plt
import os


def dice_roi(output_dir, atlas1, atlas2,png_name):
    """Calculates the dice coefficient for every ROI combination from atlas1 and atlas2

    Parameters
    ----------
    atlas1 : str
        path to first atlas to compare
    atlas2 : str
        path to second atlas to compare
    """

    if not png_name:
        #Create output name for png file
        png_name=f"DICE_{atlas1.strip('.nii.gz')}_x_{atlas2.strip('.nii.gz')}"

    at1 = nb.load(atlas1)
    at2 = nb.load(atlas2)

    atlas1 = at1.get_data()
    atlas2 = at2.get_data()
    
    labs1 = np.unique(atlas1)
    labs2 = np.unique(atlas2)

    Dice = np.zeros((labs1.size, labs2.size))

    for val1 in labs1:
        for val2 in labs2:

            dice = np.sum(atlas1[atlas2==val2]==val1)*2.0 / (np.sum(atlas1[atlas1==val1]==val1) + np.sum(atlas2[atlas2==val2]==val2))
            
            Dice[int(val1)][int(val2)]=float(dice)

            print(f'Dice coefficient for Atlas1 {val1}, Atlas2 {val2} = {dice}')

            if dice > 1 or dice < 0:
                raise ValueError(f"Dice coefficient is greater than 1 or less than 0 ({dice}) at atlas1: {val1}, atlas2: {val2}")

    
    #Generate png of heatmap

    fig, ax = plt.subplots()
    im = ax.imshow(Dice, cmap="gist_heat_r", norm=matplotlib.colors.LogNorm())

    #axes
    ax.set_xticks(np.arange(0,len(labs2), step=10))
    ax.set_yticks(np.arange(0,len(labs1)))

    
    ax.set_xticklabels(labs2[0::10])
    ax.set_yticklabels(labs1)

    ax.set_ylabel('ROIs for Yeo-17 atlas')
    ax.set_xlabel('ROIs for Schaefer-300 atlas')

    plt.setp(ax.get_xticklabels(), fontsize=6, rotation=90, ha="right", rotation_mode="anchor")
    plt.setp(ax.get_yticklabels(), fontsize=6)

    #ax.set_title(png_name)
    
    # Try to counteract the lopsided amount of ROIs between atlases
    aspect_ratio=len(labs2)/len(labs1)

    ax.set_aspect(aspect=aspect_ratio)
    #jdhao.github.io/2017/06/03/change-aspect-ratio-in-mpl

    plt.colorbar(im, aspect=30)
    fig.tight_layout()

    plt.show()

    plt.savefig(f'{output_dir}/{png_name}.png', dpi=1000)

    return Dice, labs1, labs2
    print('Done')
    
   

def main():

    parser = ArgumentParser(
        description="Script to take already MNI-aligned atlas images and generate json file information."
    )
    parser.add_argument(
        "atlas1",
        help="""The path of the mri parcellation
        file you intend to process.""",
        action="store",
    )
    parser.add_argument(
        "atlas2",
        help="""The path of the second mri parcellation
        file you intend to process.""",
        action="store",
    )
    parser.add_argument(
        "output_dir",
        help="""Path to directory you wish to store output
        heatmap.""",
        action="store",
    )
    parser.add_argument(
        "--png_name",
        help="""Name of the generated png heatmap for the Dice calculations. If
        None, the name of the file will be 'DICE_<atlas1>_x_<atlas2>.png. Default
        is None.'""",
        action="store",
        default=None,
    )
    

    # and ... begin!
    print("\nBeginning Dice ...")

    # ---------------- Parse CLI arguments ---------------- #
    result = parser.parse_args()
    atlas1 = result.atlas1
    atlas2 = result.atlas2
    output_dir = result.output_dir
    png_name = result.png_name


    # Creation of output_dir if it doesn't exit
    if not os.path.isdir(output_dir):
        os.makedirs(f"{output_dir}")


    Dice_matrix, ylabels, xlabels = dice_roi(output_dir,atlas1,atlas2, png_name)

if __name__ == "__main__":
    main()