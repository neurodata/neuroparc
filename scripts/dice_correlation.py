import nibabel as nb
import numpy as np
from argparse import ArgumentParser
import matplotlib
from matplotlib import pyplot as plt
import os
from math import floor


def dice_roi(input_dir, output_dir, atlas1, atlas2):
    """Calculates the dice coefficient for every ROI combination from atlas1 and atlas2

    Parameters
    ----------
    atlas1 : str
        path to first atlas to compare
    atlas2 : str
        path to second atlas to compare
    """

    #Create output name for png file
    yname = atlas1.split('_space-')[0]
    res=atlas1.split('space-MNI152NLin6_res-')[1]
    res=res.split('.nii')[0]
    xname = atlas2.split('_space-')[0]
    
    png_name=f"DICE_{yname}_&_{xname}_res-{res}"

    at1 = nb.load(f'{input_dir}/{atlas1}')
    at2 = nb.load(f'{input_dir}/{atlas2}')

    atlas1 = at1.get_data()
    atlas2 = at2.get_data()
    
    labs1 = np.unique(atlas1)
    labs2 = np.unique(atlas2)

    Dice = np.zeros((labs1.size, labs2.size))

    max_y=len(labs1)-1
    max_x=len(labs2)-1

    for i in range(len(labs1)):
        val1=labs1[i]
        for j in range(len(labs2)):
            val2=labs2[j]
            dice = np.sum(atlas1[atlas2==val2]==val1)*2.0 / (np.sum(atlas1[atlas1==val1]==val1) + np.sum(atlas2[atlas2==val2]==val2))
            
            Dice[int(i)][int(j)]=float(dice)

            print(f'Dice coefficient for {yname} {i} of {max_y}, {xname} {j} of {max_x} = {dice}')

            if dice > 1 or dice < 0:
                raise ValueError(f"Dice coefficient is greater than 1 or less than 0 ({dice}) at atlas1: {val1}, atlas2: {val2}")

    
    #Generate png of heatmap

    fig, ax = plt.subplots()
    im = ax.imshow(Dice, cmap="gist_heat_r", norm=matplotlib.colors.LogNorm())

    if len(labs1)<30:
        step1=1
    else:
        step1=floor(len(labs1)/30)

    if len(labs2)<30:
        step2=1
    else:
        step2=floor(len(labs2)/30)

    #axes
    ax.set_xticks(np.arange(0,len(labs2), step=step2))
    ax.set_yticks(np.arange(0,len(labs1), step=step1))

    
    ax.set_xticklabels(labs2[0::step2])
    ax.set_yticklabels(labs1[0::step1])

    ax.set_ylabel(f'ROIs for {yname} atlas')
    ax.set_xlabel(f'ROIs for {xname} atlas')

    plt.setp(ax.get_xticklabels(), fontsize=6, rotation=90, ha="right", rotation_mode="anchor")
    plt.setp(ax.get_yticklabels(), fontsize=6)

    ax.set_title(f'{yname} vs {xname}')
    
    # Try to counteract the lopsided amount of ROIs between atlases
    aspect_ratio=len(labs2)/len(labs1)

    ax.set_aspect(aspect=aspect_ratio)
    #jdhao.github.io/2017/06/03/change-aspect-ratio-in-mpl

    plt.colorbar(im, aspect=30)
    fig.tight_layout()

    plt.show()

    plt.savefig(f'{output_dir}/{png_name}.png', dpi=1000)

    #Save Dice map to csv file, comma delimited
    np.savetxt(f'{output_dir}/{png_name}.csv', Dice, delimiter=",")

    return Dice, labs1, labs2
    print('Done')
    
   

def main():

    parser = ArgumentParser(
        description="Script to take already MNI-aligned atlas images and generate json file information."
    )
    parser.add_argument(
        "input_dir",
        help="Input directory",
        action="store",
    )
    parser.add_argument(
        "atlases",
        help="""List of names of the mri parcellations
        file you intend to process. Each atlas will be compared
        to eachother, so [a,b,c] will generate axb, axc, bxc.""",
        nargs="+",
    )
    parser.add_argument(
        "output_dir",
        help="""Path to directory you wish to store output
        heatmap.""",
        action="store",
    )
    

    # and ... begin!
    print("\nBeginning Dice ...")

    # ---------------- Parse CLI arguments ---------------- #
    result = parser.parse_args()
    input_dir = result.input_dir
    atlases = result.atlases
    output_dir = result.output_dir


    # Creation of output_dir if it doesn't exit
    if not os.path.isdir(output_dir):
        os.makedirs(f"{output_dir}")

    for i in range(len(atlases)):
        for j in range(len(atlases)):
            if j > i:
                Dice_matrix, ylabels, xlabels = dice_roi(input_dir,output_dir,atlases[i],atlases[j])

if __name__ == "__main__":
    main()