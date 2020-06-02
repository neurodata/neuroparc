import nibabel as nb
import numpy as np


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

    for val1 in labs1:
        for val2 in labs2:

            dice = np.sum(atlas1[atlas2==val2]==val1)*2.0 / (np.sum(atlas1[atlas1==val1]==val1) + np.sum(atlas2[atlas2==val2]==val2))

    #k=1
    # segmentation
    #seg = np.zeros((100,100), dtype='int')
    #seg[30:70, 30:70] = k
    # ground truth
    #gt = np.zeros((100,100), dtype='int')
    #gt[30:70, 40:80] = k
    #dice = np.sum(seg[gt==k]==k)*2.0 / (np.sum(seg[seg==k]==k) + np.sum(gt[gt==k]==k))

    print(f'Dice similarity score is {dice}')



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
        heatmap."""
        action="store"
    )
    

    # and ... begin!
    print("\nBeginning Dice ...")

    # ---------------- Parse CLI arguments ---------------- #
    result = parser.parse_args()
    atlas1 = result.atlas1
    atlas2 = result.atlas2
    output_dir = result.output_dir


    # TODO: Add creation of output_dir


    dice_roi(atlas1,atlas2)