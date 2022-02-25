# Neuroparc Atlas Data Structure v.0.0.1

The following specification for atlases submitted to Neuroparc must be followed or the submission will not be accepted. Any suggestions for changes can be directed towards the maintainers of Neuroparc on the GitHub issues page. This specification is a work-in-progress and relies on community contribution. Most of it is based on the BIDS format for MRI files: http://bids.neuroimaging.io/

There are two main files required for submission of an atlas. The structure should appear as follows:

```
Atlas_Name
|-- <atlas_name>_space-<space_name>_res-<resolution>.nii.gz
`-- <atlas name>-regions-1x1x1.json
```

The entire folder will then be placed under the appropriate species subfolder.

## File #1: Atlas File

File Name: `<atlas_name>_space-<space_name>_res-<resolution>.nii.gz`

Must be in the NIFTI format and capable of being opened by any standard MRI viewer (MRIcron, FSLeyes, MIPAV, etc.). The resolution is specified in the name of the file as well as the space it is defined in. For the atlas name, all spaces should be replaced with underscores or the name should use proper camelCase. The same applies to the space name.

## File 2: Atlas Information

File Name: `<atlas name>-regions-1x1x1.json`
```
{
    "MetaData": {
        "AtlasName": {Name},
        "Description": {Description},
        "Native Coordinate Space": {Coordinate Space},
        "Hierarchical": {yes, no},
        "Symmetrical": {yes, no},
        "Number of Regions": {# of regions},
        "Average Volume Per Region": {Ave Vol},
        "Year Generated": {Year},
        "Generation Method": {Method},
        "Source": {URL}
    },
    "rois": {
	"{x}": {
            "label": {},
	    ["description"] = {}
	    ["color"]: [{R}, {G}, {B}],
            "center": [{x}, {y}, {z}],
            "size": {size}
        },
	...
     }
}

Fields (all required unless specified):
- Region <Number of region>
    - label: Provide a common name for the region. Numerical values are acceptable if the atlas is generative.
    - OPTIONAL description: If desired, a brief description of the importance of the region can be specified here.
    - OPTIONAL color: If a specific color is required for the region, then use RGB values to define it with comma-separated values enclosed by square brackets. ([R, G, B])
    - center: The center of the region should be defined relative to the coordinate system the atlas is in and the resolution of the atlas.
    - size: Size must be specified in voxels according to the resolution in the file name.
- MetaData
    - AtlasName: This should be the same as in the filename.
    - Description: Provide a use case for the atlas that someone looking through the list of atlases can understand
Native Coordinate Space: The coordinate space the atlas is defined in (i.e. Talairach or MNI)
    - OPTIONAL Hierarchical: If the atlas consists of hierarchical components (meaning there are subregions), this value should be 1 and 0 if otherwise. Will be calculated if not provided.
    - OPTIONAL Symmetrical: If the atlas is designed to be symmetrical, this value should be 1 and 0 otherwise. Will be calculated if not provided.
    - OPTIONAL Number of Regions: The number of regions defined by the atlas, not including empty space. Will be calculated if not provided
    - OPTIONAL Average Volume Per Region: The average volume of all regions, not including empty space. Will be calculated if not provided.
    - OPTIONAL Year Generated: The year the atlas was first created, not the date of submission or the date of publication.
    - OPTIONAL Generation Method: A brief (2-3 sentences) description of the method used to produce the atlas.
    - OPTIONAL Source: If the atlas has been published, please link the paper here if it is available.
