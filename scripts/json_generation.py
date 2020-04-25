import nibabel as nb
import numpy as np
import json
import csv
import os
import glob
from nilearn import plotting as nip
from nilearn import image
from argparse import ArgumentParser


def get_centers(brain):
    """
    Get coordinate centers given a nifti image loaded with nibabel
    
    Returns a dictionary of label: coordinate as an [x, y, z] array
    """
    dat = brain.get_data()
    labs = np.unique(dat)
    labs = labs[labs != 0]
    # Line below throwing memory error. I will likely calculate each layer one at a time
    # and find the center
    fd_dat = np.stack([np.asarray(dat == lab).astype('float64') for lab in labs], axis=3)
    parcels = nb.Nifti1Image(dataobj=fd_dat, header=brain.header, affine=brain.affine)
    regions_imgs = image.iter_img(parcels)
    # compute the centers of mass for each ROI
    coords_connectome = [nip.find_xyz_cut_coords(img) for img in regions_imgs]
    return dict(zip(labs, coords_connectome))

def main():

    parser = ArgumentParser(
        description="Script to take already MNI-aligned atlas images and generate json file information."
    )
    parser.add_argument(
        "--input_file",
        help="""The directory with the mri parcellation
        files you intend to process are.""",
        action="store",
        default="/data/neuroparc/hemispheric_space-MNI152NLin6_res-1x1x1.nii.gz"
    )
    parser.add_argument(
        "--output_dir",
        help="""The directory to store the generated nii.gz and/or json file(s).""",
        action="store",
        default="/data/neuroparcdump"
    )
    parser.add_argument(
        "--MNI_align",
        help="Whether to align atlas to MNI before generating json file",
        action="store",
        default=False,
    )
    parser.add_argument(
        "--reference_brain",
        help="Path for reference image you are registering your atlas too",
        action="store",
        default="/data/neuroparc/atlases/reference_brains/MNI152NLin6_res-1x1x1_T1w.nii.gz"
    )
    parser.add_argument(
        "--voxel_size",
        help="Desired resample voxel size, default is 1",
        action="store",
        default=1,
    )
    parser.add_argument(
        "--label_csv",
        help="csv file containing the information",
        action="store",
        default="/data/neuroparc/scripts/sample_csv.csv",
    )



    # and ... begin!
    print("\nBeginning neuroparc ...")

    # ---------------- Parse CLI arguments ---------------- #
    result = parser.parse_args()
    input_file = result.input_file
    output_dir = result.output_dir
    ref_brain = result.reference_brain
    vox_size = result.voxel_size
    mni_align = result.MNI_align
    csv_f = result.label_csv


    # Load and organize csv for use in json creation
    if csv:
        biglist=[]
        with open(csv_f, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                biglist.append(row[0])
                biglist.append(row[1])
            csv_dict = {biglist[i]: biglist[i+1] for i in range(0, len(biglist), 2)}


    if mni_align:
        # align input file to the dataset grid of "master"
        cmd = f"3dresample -input {filename} -prefix {output_name} -master {ref_brain}"
        subprocess.call(cmd, shell=True)
        # register image to atlas
        cmd = f"flirt -in {output_name} -out {output_reg} -ref {ref_brain} -applyisoxfm {vox_size} -interp nearestneighbour"
        subprocess.call(cmd, shell=True)
        
        # Change datatype of resampled file to 768?
        im = nb.load(output_name)
        newdat = im.get_data().astype(np.uint32)
        im.header['datatype'] = 768
        nb.save(nb.Nifti1Image(dataobj=newday, header=im.header, affine=im.affine), filename=output_name)

        # Change datatype of registered file to 768?
        im.nb.load(output_reg)
        newdat=im.get_data().astype(np.uint32)
        im.header['datatype'] = 768
        nb.save(nb.Nifti1Image(dataobj=newdat, header=im.header, affine=im.affine), filename=output_reg)

    #Convert_schaeffer.sh
    #for f in Schaefer*nii.gz; do
	#    echo "python -c \"import nibabel as nb; import numpy as np; 
    #    im = nb.load('$f'); 
    #    newdat = im.get_data().astype(np.uint32);
    #    im.header['datatype'] = 768;
    #    nb.save(nb.Nifti1Image(dataobj=newdat, header=im.header, affine=im.affine), filename='$f')""

    #Converter.sh
    #for f in yeo-*1x1x1*nii.gz; do
	# "3dresample -input $f -prefix new.nii.gz -master ../atlas/MNI152NLin6_res-1x1x1_T1w.nii.gz"
	# "mv new.nii.gz $f"
	# newf="${f/1x1x1/2x2x2}"
	#"flirt -in $f -out $newf -ref ../atlas/MNI152NLin6_res-2x2x2_T1w.nii.gz -applyisoxfm 2 -interp nearestneighbour"
	#"python -c \"import nibabel as nb; import numpy as np; 
    # im = nb.load('$f');
    # newdat = im.get_data().astype(np.uint32);
    # im.header['datatype'] = 768;
    # nb.save(nb.Nifti1Image(dataobj=newdat, header=im.header, affine=im.affine), filename='$f')""
	# im = nb.load('$newf'); 
    # newdat = im.get_data().astype(np.uint32); 
    # im.header['datatype'] = 768; 
    # nb.save(nb.Nifti1Image(dataobj=newdat, header=im.header, affine=im.affine), filename='$newf')\""



    specparc = ['desikan', 'tissue', 'DK', 'pp264']
    specdir = '../atlases/label/Human'
    jsdir = '../atlases/label/Human/label_updated'
    outdir=output_dir
    #outdir = '../atlases/label/Human/label_updated2'
    
    brainglob = input_file
    #brainglob = glob.glob(os.path.join(input_dir, '*.nii.gz'))
    #jsonglob = glob.glob(os.path.join(jsdir, '*.json'))
    
    # iterate over the brains
    for brainf in brainglob:
        # get the name of the particular parcel
        brain_name = str.split(os.path.basename(brainf), '.')[0]
        bname = str.split(brain_name, '_')[0]
        jsout = os.path.join(outdir, "{}.json".format(brain_name))
        parcel_im = nb.load(brainf)
        parcel_centers = get_centers(parcel_im)
        if csv:
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
        else:
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



if __name__ == "__main__":
    main()