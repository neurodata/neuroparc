for f in yeo-*1x1x1*nii.gz; do
	echo "3dresample -input $f -prefix new.nii.gz -master ../atlas/MNI152NLin6_res-1x1x1_T1w.nii.gz"
	echo "mv new.nii.gz $f"
	newf="${f/1x1x1/2x2x2}"
	echo "flirt -in $f -out $newf -ref ../atlas/MNI152NLin6_res-2x2x2_T1w.nii.gz -applyisoxfm 2 -interp nearestneighbour"
	echo "python -c \"import nibabel as nb; import numpy as np; im = nb.load('$f'); newdat = im.get_data().astype(np.uint32); im.header['datatype'] = 768; nb.save(nb.Nifti1Image(dataobj=newdat, header=im.header, affine=im.affine), filename='$f')\""
	echo "python -c \"import nibabel as nb; import numpy as np; im = nb.load('$newf'); newdat = im.get_data().astype(np.uint32); im.header['datatype'] = 768; nb.save(nb.Nifti1Image(dataobj=newdat, header=im.header, affine=im.affine), filename='$newf')\""
done
