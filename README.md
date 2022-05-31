Convert anatomy archives to BIDS format. Convert DICOM to NIFTI on the way.

Requirements
------------
- unix shell (cp, rm commands + possibility to install unzip and unrar)
- anaconda\miniconda python installation

0. Download the code and change working directory to its root folder

```bash
git clone https://github.com/dmalt/MRI_metacognition.git
cd MRI_metacognition
```

1. Create and activate conda environment
```bash
conda env create -f environment.yml
conda activate mri
```
2. Install unzip, unrar and docker

Folders structure
-----------------

- `sourcedata`\
    Orignially collected MRI images in different formats packaged in zip and rar archives
- `sourcedata/code`\
    Code used to organize sourcedata into folders. Inputs for this code are not provided and it
    exists only for reference
- `rawdata`\
    MRI images converted to NIFTI and stored as [BIDS](https://bids.neuroimaging.io/)-like dataset.
    We don't provide the actual data files since they can be recovered with a pipeline in `rawdata/code`
- `rawdata/code`\
    Code used to convert sourcedata to BIDS format
- `rawdata/derivatives`\
    Derivative datasets for rawdata
- `rawdata/derivatives/fsf`\
    Freesurfer reconstruction pipeline
- `rawdata/derivatives/fsf/code`\
    Code for freesurfer reconstruction

Launch
------
To run the sourcedata-BIDS conversion pipeline, go to `rawdata/code` and run
```bash
doit
```

Adding new subject
------------------
To add a new subject, place the anatomy archive to `../../sourcedata/sub-<subject_id>/anat`
and run the first two pipeline steps:
```bash
doit unarchive
doit convert
```

Check `../sub-<subject_id>/anat` folder for the newly added subject. It should have 2 files:
`sub-<subject_id>_T1w.json` and `sub-<subject_id>_T1w.nii.gz`. If these two files are present, it's all good.
Run the whole pipeline again to clean the temporary folders:

```bash
doit
```

### In case the folder is empty

**The first possibility** is that series description of the new image differs
from the images of already added subjects. This is normal if the MRI was
aquired in a different setup or hospital than those for other subjects.

Series descriptions are selected manually and stored at `dcm2bids_config.json`.
To update it, first check `../tmp_dcm2bids/sub-<subject_id>` folder. It should
contain all images found by `dcm2niix` with the corresponding `.json` sidecar files.

Here we need to find an actual MRI data. Among the available jsons select the
value of `SeriesDescription` that matches an actual data file. Note, that for
MRI acquisition there are usually several "support" image sequencies, e.g.
lokalizers, which we don't need. One way to find the correct image is to open
its `.nii.gz` file in one of the NIFTI viewers available [online](https://socr.umich.edu/HTML5/BrainViewer/).

Once the correct series is found, open its `.json` file in a text editor and find the `SeriesDescription` field.
Use this field to append a section with a new selection rule to the `dcm2bids_config.json` like this:

```json
{
"dataType": "anat",
"modalityLabel": "T1w",
"criteria": {
    "SeriesDescription": "t1_mpr_ns_sag_p2_iso",
    }
}
```

`dcm2bids` will use this new rule to select a proper series by its description.

Usually "criteria" based only on "SeriesDescription" is enough, but in case several files
are selected you'll need to experiment with a more strict criteria. For that, refer to
the `dcm2bids` [documentation](https://unfmontreal.github.io/Dcm2Bids/docs/how-to/create-config-file/)


