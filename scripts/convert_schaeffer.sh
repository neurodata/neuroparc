for f in Schaefer*nii.gz; do
	echo "python -c \"import nibabel as nb; import numpy as np; im = nb.load('$f'); newdat = im.get_data().astype(np.uint32); im.header['datatype'] = 768; nb.save(nb.Nifti1Image(dataobj=newdat, header=im.header, affine=im.affine), filename='$f')\""
done
