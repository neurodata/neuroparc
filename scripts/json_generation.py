import nibabel as nb
import numpy as np
import json
import csv
import os
import glob
import subprocess
import sys
from datetime import datetime
from nilearn import plotting as nip
from nilearn import image
from argparse import ArgumentParser


def get_centers(brain, orig_labs):
    """
    Get coordinate centers given a nifti image loaded with nibabel
    
    Returns a dictionary of label: coordinate as an [x, y, z] array
    """
    dat = brain.get_data()
    
    labs, size = np.unique(dat, return_counts=True)

    size=dict(zip(labs,size))
        
    # Bit of a clumsy stop-gap for correcting for lost ROIs due to resampling/registration
    for n in orig_labs:
        if not size.get(n):
            size[n] = None

    coords_connectome = []
    for lab in labs:
        fd_dat = np.asarray(dat == lab).astype('float64')
        parcel = nb.Nifti1Image(dataobj=fd_dat, header=brain.header, affine=brain.affine)
        coords_connectome.append(nip.find_xyz_cut_coords(parcel))

    return dict(zip(labs, coords_connectome)), size

def main():

    parser = ArgumentParser(
        description="Script to take already MNI-aligned atlas images and generate json file information."
    )
    parser.add_argument(
        "input_file",
        help="""The path of the mri parcellation file you intend to process.
        If you only specify this value, 'output_dir', and optionally '--label_csv',
        then a JSON file will be generate without manipulating this input file.""",
        action="store",
    )
    parser.add_argument(
        "output_dir",
        help="""The directory to store the generated nii.gz and/or json file(s).""",
        action="store",
    )
    parser.add_argument(
        "--output_name",
        help="""Name assigned to both the processed parcellation file and its corresponding,
        json label file. Do not include the file type (nii.gz, nii, or json).
        If None, 'input_file' and 'reference_brain' names will be combined to
        make <input_file>_<ref_brain>.nii.gz/.json. Default is None.""",
        action="store",
        default=None,
    )
    parser.add_argument(
        "--ref_brain",
        help="""Path for reference image you wish to register your parcellation too,
        be sure that it has the correct voxel size you want your output atlas file to have.
        If None, resampling and registration will not be done. Default is None.""",
        action="store",
        default=None,
    )
    parser.add_argument(
        "--voxel_size",
        help="""Voxel size (1,2,4 mm^3, etc.) of the ref_brain image specified in 'ref_brain'. This value must be
        input if you wish to run resampling and registration. Default is 1.""",
        action="store",
        default='1',
    )
    parser.add_argument(
        "--label_csv",
        help="csv file containing the ROI label information for the parcellation file, default is None",
        action="store",
        default=None,
    )


    # and ... begin!
    print("\nBeginning neuroparc ...")

    # ---------------- Parse CLI arguments ---------------- #
    result = parser.parse_args()
    input_file = result.input_file
    output_dir = result.output_dir
    output_name = result.output_name
    ref_brain = result.ref_brain
    vox_size = result.voxel_size
    csv_f = result.label_csv

    #If you have an input file, reference file, and no output name
    if input_file and ref_brain and not output_name: 
        inp = input_file.split("/")[-1]
        inp = inp.split(".nii")[0]
        refp = ref_brain.split("/")[-1]
        refp = refp.split(".nii")[0]
        output_name = f"{inp}_{refp}"

    # Load and organize csv for use in json creation
    if csv_f:
        biglist=[]
        with open(csv_f, newline='', encoding = 'utf-8-sig') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                biglist.append(row[0])
                biglist.append(row[1])
            csv_dict = {biglist[i]: biglist[i+1] for i in range(0, len(biglist), 2)}

    orig = nb.load(input_file)
    dat = orig.get_data()
    orig_labs, _ = np.unique(dat, return_counts=True)

    if ref_brain:
        # align input file to the dataset grid of the reference brain "master"
        cmd = f"3dresample -input {input_file} -prefix {output_dir}/{output_name}.nii.gz -master {ref_brain}"
        subprocess.call(cmd, shell=True)
        # Change datatype of resampled file to 768?
        im = nb.load(f"{output_dir}/{output_name}.nii.gz")
        newdat = im.get_data().astype(np.uint32)
        im.header['datatype'] = 768
        nb.save(nb.Nifti1Image(dataobj=newdat, header=im.header, affine=im.affine), filename=f"{output_dir}/{output_name}.nii.gz")

        #Register atlas to reference brain
        output_reg = f"{output_dir}/reg_{output_name}.nii.gz"
        # register image to atlas
        cmd = f"flirt -in {output_dir}/{output_name}.nii.gz -out {output_reg} -ref {ref_brain} -applyisoxfm {vox_size} -interp nearestneighbour"
        subprocess.call(cmd, shell=True)
        
        # Change datatype of registered file to 768?
        im = nb.load(f"{output_reg}")
        newdat=im.get_data().astype(np.uint32)
        im.header['datatype'] = 768
        nb.save(nb.Nifti1Image(dataobj=newdat, header=im.header, affine=im.affine), filename=output_reg)

    
    if not ref_brain: #If you just want a json file to be made, outputname will = input_file name
        if not output_name:
            inp = input_file.split("/")[-1]
            inp = inp.split(".nii")[0]
            output_name=inp

        output_reg = input_file #Have the parcel_centers run on input file without any resampling/registering



    jsout = f"{output_dir}/{output_name}.json"
    js_contents={"MetaData":{},"rois":{}}
    roi_sum=0
    count=0
    now = datetime.now()
    parcel_im = nb.load(output_reg)
    parcel_centers, size= get_centers(parcel_im,orig_labs)
    if csv_f:
    # find a corresponding json file
        js_contents['rois'][str(0)] = {"label": "empty", "center":None}
        for (k, v) in csv_dict.items():
            k=int(k)
            try:
                js_contents['rois'][str(k)] = {"label": v, "center": parcel_centers[k], "size":int(size[k])}
                roi_sum=roi_sum+size[k]
                count=count+1
            except KeyError:
                js_contents['rois'][str(k)] = {"label": v, "center": None, "size": None}
            except TypeError:
                js_contents['rois'][str(k)] = {"label": v, "center": None, "size": None}

            
    else:
        js_contents['rois'][str(0)] = {"label": "empty", "center":None}
        for (k, v) in parcel_centers.items():
            k=int(k)
            try:
                js_contents['rois'][str(k)] = {"label": None,"center": parcel_centers[k],"size":int(size[k])}
                roi_sum=roi_sum+size[k]
                count=count+1
            except KeyError:
                js_contents['rois'][str(k)] = {"label": None, "center": None, "size": None}
            except TypeError:
                js_contents['rois'][str(k)] = {"label": None, "center": None, "size": None}
        
    #Atlas-wide Metadata
    js_contents["MetaData"] = {"AtlasName": "", "Description": '',
    "Native Coordinate Space": '', "Hierarchical": '', "Symmetrical": '',
    "Number of Regions": str(count), "Average Volume Per Region": str(float(roi_sum/count)), "Year Generated": str(now.year),
    "Generation Method":'', "Source":''}
                
    with open(jsout, 'w') as jso:
        json.dump(js_contents, jso, indent=4)
            
if __name__ == "__main__":
    main()