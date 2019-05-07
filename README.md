# Neuroparc


This repository contains a number of useful parcellations, templates, masks, and transforms to (and from) MNI152NLin6 space. The files are named according to the BIDs specification.

![](https://github.com/NeuroDataDesign/the-ents/blob/explore-atlases/atlases/Results/brainAtlases_color_wRegions.png)


## Atlas Info Summary

<a name="Table"></a>

| Atlas Name | # Regions | Symmetrical? | Hierarchical? | Labelled? | Generation Method | Average Vol/Region | Native coordinate space | Description | Sources | Year of Origin |
|------------------------------|-----------|--------------|---------------|-----------|---------------------------------------------------------------------------------------------------------------------|--------------------|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------|----------------|
| Tissue | 3 |  | No | No |  | 609031.667 |  |  | (Tissue-based segmentation: WM, GM, CSF) | 2018 |
| Yeo 7 | 7 | Yes | No | Yes | Clustered to identify networks of functionally coupled regions | 75383.571 | FreeSurfer surface space | Local networks confined to sensory and motor cortices, functional connectivity followed topographic representations across adjacent areas | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3174820/ | 2011 |
| Yeo 7 Liberal | 7 | Yes | No | Yes | Clustered to identify networks of functionally coupled regions | 150676.143 | FreeSurfer surface space | Local networks confined to sensory and motor cortices, functional connectivity followed topographic representations across adjacent areas | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3174820/ | 2011 |
| Yeo 17 | 17 | Yes | No | Yes | Clustered to identify networks of functionally coupled regions | 31040.294 | FreeSurfer surface space | Local networks confined to sensory and motor cortices, functional connectivity followed topographic representations across adjacent areas | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3174820/ | 2011 |
| Yeo 17 Liberal | 17 | Yes | No | Yes | Clustered to identify networks of functionally coupled regions | 62043.118 | FreeSurfer surface space | Local networks confined to sensory and motor cortices, functional connectivity followed topographic representations across adjacent areas | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3174820/ | 2011 |
| Brodmann | 40 | Yes | Yes | No | Brodman areas separated by gyri | 32978.512 |  | Corticall parcellation separating regions based on cellular morphology and organization | http://digital.zbmed.de/zbmed/id/554966 | 1909 |
| HarvardOxford | 48 | No | Yes | Yes |  | 21966.104 |  |  | http://neuro.imm.dtu.dk/wiki/Harvard-Oxford_Atlas |  |
| JHU | 48 | Yes | No | Yes | One subject manually labelled and warped to 29 other adult atlases (Large Deformation Diffeomorphic Metric Mapping) | 3541.792 |  | A small version of a larger (289 ROI) atlas composed based on parcellation of deep white matter. Split into 4 groups: Tracts in the brainstem, projection fibers, association fibers, and commisural fibers | https://www.ncbi.nlm.nih.gov/pubmed/14645885 | 2004 |
| Princeton | 49 | Yes | Yes | Yes |  | 1217.388 |  |  | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4585523/ | 2015 |
| pp264 | 58 | No |  | No |  | 470.966 |  |  | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3222858/ |  |
| Desikan | 70 | Yes | No | No | Anatomical Landmarks based on gyri. Averaged based on majority voting | 24786.857 |  | Surface parcellation | https://www.sciencedirect.com/science/article/pii/S1053811906000437?via%3Dihub | 2006 |
| AAL | 116 | No | No | Yes | Delineated with respect to anatomical landmarks (following sulci course in brain) | 12758.353 | MNI | Automated Anatomical Labelling | https://www.ncbi.nlm.nih.gov/pubmed/11771995 | 2002 |
| CPAC200 | 200 | No |  | No |  | 5860.755 |  |  | https://github.com/FCP-INDI/C-PAC | 2018 |
| Schaefer2018 - 200 | 200 | No | No | No | Automatic using gwMRF | 5278.425 |  | Gradient-weighted Markov Random Fields (gwMRF) to group similar fMRI regions (dependent on # of regions specified) | http://people.csail.mit.edu/ythomas/publications/2018LocalGlobal-CerebCor.pdf | 2017 |
| Schaefer2018 - 300 | 300 | No | No | No | Automatic using gwMRF | 3518.95 |  | Gradient-weighted Markov Random Fields (gwMRF) to group similar fMRI regions (dependent on # of regions specified) | http://people.csail.mit.edu/ythomas/publications/2018LocalGlobal-CerebCor.pdf | 2017 |
| Glasser | 360 | Yes | Yes | Yes | Semi-automated. Separated based on function, connectivity, cortical architecture, topography, and expert analysis | 521.994 | MNI | Cortical parcellation from multi-modal images of 210 adults in HCP | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4990127/ | 2016 |
| Schaefer2018 - 400 | 400 | No | No | No | Automatic using gwMRF | 2639.213 |  | Gradient-weighted Markov Random Fields (gwMRF) to group similar fMRI regions (dependent on # of regions specified) | http://people.csail.mit.edu/ythomas/publications/2018LocalGlobal-CerebCor.pdf | 2017 |
| Schaefer2018 - 1000 (Yeo 17) | 1000 | No | No | No | Automatic using gwMRF | 1055.685 | Yeo 17 | Gradient-weighted Markov Random Fields (gwMRF) to group similar fMRI regions (dependent on # of regions specified) | http://people.csail.mit.edu/ythomas/publications/2018LocalGlobal-CerebCor.pdf | 2017 |
| Schaefer2018 - 1000 (Yeo 7) | 1000 | No | No | No | Automatic using gwMRF | 1055.685 | Yeo 7 | Gradient-weighted Markov Random Fields (gwMRF) to group similar fMRI regions (dependent on # of regions specified) | http://people.csail.mit.edu/ythomas/publications/2018LocalGlobal-CerebCor.pdf | 2017 |
| Schaefer2018 - 1000 | 1000 | No | No | No | Automatic using gwMRF | 1055.685 |  | Gradient-weighted Markov Random Fields (gwMRF) to group similar fMRI regions (dependent on # of regions specified) | http://people.csail.mit.edu/ythomas/publications/2018LocalGlobal-CerebCor.pdf | 2017 |
| Slab | 1068 |  |  | No |  | 493.719 |  |  | https://www.nitrc.org/projects/kessler_jama16/  |  |
| Talairach | 1105 | No | Yes | Yes | Semi-automated? | 1698.114 | Talairach coordinates | A hierarchical atlas split into 5 leves: Hemisphere, Lobe, Gyrus, Tissue Type, and Cell Type | https://www.ncbi.nlm.nih.gov/pubmed/7008525 | 1980 |

