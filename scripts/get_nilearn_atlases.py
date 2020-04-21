# Ganesh Arvapalli

# Script to download all the Nilearn atlases

import nilearn.datasets as nd

def main():
    nd.fetch_atlas_craddock_2012(data_dir=".")
    nd.fetch_atlas_destrieux_2009(data_dir=".")
    hox_names = ["cort-maxprob-thr0-1mm",  "cort-maxprob-thr0-2mm",
        "cort-maxprob-thr25-1mm", "cort-maxprob-thr25-2mm",
        "cort-maxprob-thr50-1mm", "cort-maxprob-thr50-2mm",
        "sub-maxprob-thr0-1mm",  "sub-maxprob-thr0-2mm",
        "sub-maxprob-thr25-1mm", "sub-maxprob-thr25-2mm",
        "sub-maxprob-thr50-1mm", "sub-maxprob-thr50-2mm",
        "cort-prob-1mm", "cort-prob-2mm",
        "sub-prob-1mm", "sub-prob-2mm"]
    for i in hox_names:
        nd.fetch_atlas_harvard_oxford(atlas_name=i, data_dir=".")
    nd.fetch_atlas_msdl(data_dir=".")
    power2011 = nd.fetch_coords_power_2011()
    nd.fetch_atlas_smith_2009(data_dir=".")
    nd.fetch_atlas_yeo_2011(data_dir=".")
    nd.fetch_atlas_aal(data_dir=".")
    nd.fetch_atlas_basc_multiscale_2015(data_dir=".")
    nd.fetch_atlas_allen_2011(data_dir=".")
    nd.fetch_atlas_pauli_2017(data_dir=".")
    dosenbach2010 = nd.fetch_coords_dosenbach_2010()
    print(dosenbach2010)
    nd.fetch_icbm152_2009(data_dir=".")
    nd.fetch_icbm152_brain_gm_mask(data_dir=".")
    nd.fetch_localizer_button_task(data_dir=".")
    nd.fetch_localizer_calculation_task(data_dir=".")
    nd.fetch_miyawaki2008(data_dir=".")
    nd.fetch_surf_fsaverage(data_dir=".")
    nd.fetch_atlas_surf_destrieux(data_dir=".")
    levels = ['hemisphere', 'lobe', 'gyrus', 'tissue', 'ba']
    for i in levels:
        nd.fetch_atlas_talairach(level_name=i, data_dir=".")
    nd.fetch_atlas_schaefer_2018(data_dir=".")




if __name__ == "__main__": main()