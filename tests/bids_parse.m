% test script to ensure that all files are BIDS friendly enough to be parsed by BIDS-matlab

this_dir = fileparts(mfilename('fullpath'));

label_folder = fullfile(this_dir, '..', 'atlases', 'label', 'Human');

files = bids.internal.file_utils('FPList', label_folder, '^*.nii.gz');

for i = 1:size(files, 1)
  
  this_file = deblank(files(i, :));
  
  try
    bids.File(this_file, 'tolerant', false, 'verbose', true);
  catch
    fprintf(1, '%s is not BIDS friendly\n', bids.internal.file_utils(this_file, 'filename'));
  end
  
end