import nibabel as nb
import numpy as np
import json
import os
import glob
from nilearn import plotting as nip
from nilearn import image


def get_centers(brain):
    """
    Get coordinate centers given a nifti image loaded with nibabel
    
    Returns a dictionary of label: coordinate as an [x, y, z] array
    """
    dat = brain.get_data()
    labs = np.unique(dat)
    labs = labs[labs != 0]
    fd_dat = np.stack([np.asarray(dat == lab).astype('float64') for lab in labs], axis=3)
    parcels = nb.Nifti1Image(dataobj=fd_dat, header=brain.header, affine=brain.affine)
    regions_imgs = image.iter_img(parcels)
    # compute the centers of mass for each ROI
    coords_connectome = [nip.find_xyz_cut_coords(img) for img in regions_imgs]
    return dict(zip(labs, coords_connectome))

def main():
    labdir = './label/'
    specparc = ['desikan', 'tissue', 'DK', 'pp264']
    specdir = './label'
    jsdir = './label/label_updated'
    outdir = './label/label_updated2'
    brainglob = glob.glob(os.path.join(labdir, '*.nii.gz'))
    jsonglob = glob.glob(os.path.join(jsdir, '*.json'))
    # iterate over the brains
    for brainf in brainglob:
        # get the name of the particular parcel
        brain_name = str.split(os.path.basename(brainf), '.')[0]
        bname = str.split(brain_name, '_')[0]
        jsout = os.path.join(outdir, "{}.json".format(brain_name))
        parcel_im = nb.load(brainf)
        parcel_centers = get_centers(parcel_im)
        if bname in specparc:
            # find a corresponding json file
            jsf = os.path.join(specdir, "{}.json".format(brain_name))
            with open(jsf) as js:
                js_contents = json.load(js)
                for (k, v) in js_contents.items():
                    try:
                        js_contents[k] = {"center": parcel_centers[int(k)]}
                    except KeyError:
                        js_contents[k] = {"center": None}
                with open(jsout, 'w') as jso:
                    json.dump(js_contents, jso, indent=4)
        else:
            jsf = os.path.join(jsdir, "{}.json".format(brain_name))
            with open(jsf) as js:
                js_contents = json.load(js)
                for (k, v) in js_contents.items():
                    try:
                        js_contents[k] = {"label": v['region'], "center": parcel_centers[int(k)]}
                    except KeyError:
                        js_contents[k] = {"label": v['region'], "center": None}
                with open(jsout, 'w') as jso:
                    json.dump(js_contents, jso, indent=4)
