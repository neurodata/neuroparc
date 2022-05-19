% test script to ensure that all files are BIDS friendly enough to be parsed by BIDS-matlab

this_dir = fileparts(mfilename('fullpath'));

label_folder = fullfile(this_dir, '..', 'atlases', 'label', 'Human');

reference_folder = fullfile(this_dir, '..', 'atlases', 'reference_brains');

mask_folder = fullfile(this_dir, '..', 'atlases', 'mask');

test_folder(label_folder);
test_folder(reference_folder);
test_folder(mask_folder);

%%

function test_folder(folder)
    files = bids.internal.file_utils('FPList', folder, '^*.nii.gz');

    for i = 1:size(files, 1)

        this_file = deblank(files(i, :));

        try
            bids.File(this_file, 'tolerant', false, 'verbose', true);
        catch
            fprintf(1, '%s is not BIDS friendly\n', ...
                    bids.internal.file_utils(this_file, 'filename'));
        end

    end
end
