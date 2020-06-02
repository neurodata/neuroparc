import nibabel as nb
import numpy as np
from argparse import ArgumentParser
from matplotlib import pyplot as plt


def dice_roi(atlas1, atlas2):
    """Calculates the dice coefficient for every ROI combination from atlas1 and atlas2

    Parameters
    ----------
    atlas1 : str
        path to first atlas to compare
    atlas2 : str
        path to second atlas to compare
    """

    at1 = nb.load(atlas1)
    at2 = nb.load(atlas2)

    atlas1 = at1.get_data()
    atlas2 = at2.get_data()
    
    labs1 = np.unique(atlas1)
    labs2 = np.unique(atlas2)

    Dice = np.zeros((labs1.size +1, labs2.size +1))

    for val1 in labs1:
        for val2 in labs2:

            dice = np.sum(atlas1[atlas2==val2]==val1)*2.0 / (np.sum(atlas1[atlas1==val1]==val1) + np.sum(atlas2[atlas2==val2]==val2))

            Dice[int(val1)][int(val2)]=float(dice)

            print(f'Dice coefficient for Atlas1 {val1}, Atlas2 {val2} = {dice}')

            if dice >= 1 or dice < 0:
                raise ValueError(f"Dice coefficient is greater than 1 or less than 0 ({dice}) at atlas1: {val1}, atlas2: {val2}")

    
    #Generate png of heatmap

    fig, ax = plt.subplots()
    im = ax.imshow(Dice)

    #axes
    ax.set_xticks(np.arange(len(labs2)))
    ax.set_yticks(np.arange(len(labs1)))

    ax.set_xticklabels(labs2)
    ax.set_yticklabels(labs1)

    plt.setp(ax.get_xticklabels(), fontsize=4, rotation=45, ha="right", rotation_mode="anchor")
    plt.setp(ax.get_yticklabels(), fontsize=4)
    
    ax.set_aspect(aspect=0.3)
    #jdhao.github.io/2017/06/03/change-aspect-ratio-in-mpl

    plt.show()

    plt.savefig('/outside/woop3.png', dpi=800)

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
    

    # and ... begin!
    print("\nBeginning Dice ...")

    # ---------------- Parse CLI arguments ---------------- #
    result = parser.parse_args()
    atlas1 = result.atlas1
    atlas2 = result.atlas2
    output_dir = result.output_dir


    # TODO: Add creation of output_dir


    Dice_matrix, ylabels, xlabels = dice_roi(atlas1,atlas2)

if __name__ == "__main__":
    main()