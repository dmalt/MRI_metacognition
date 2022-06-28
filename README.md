A complete anatomies processing path from an MRI images archive to the
source-analyses-ready freesurfer cortical reconstruction.

The pipeline uses [DVC](https://dvc.org/) to store the files,
[doit](https://pydoit.org/) to automate the processing steps and a custom
[docker](https://www.docker.com/) image for freesurfer-dependent operations.
Folders structure is inspired by, but doesn't follow strictly, the
[BIDS](https://bids.neuroimaging.io/) format.

Overview
--------
The pipeline provides a general way to prepare MRI images for source analyses
with MNE-Python. It transforms MRI image series in possibly different formats
to the BIDS-friendly NIFTI, runs freesurfer's recon-all and computes additional
bem surfaces needed for source analyses with MNE-Python freesurfer-dependent
command-line tools.

This repo's folders structure is as follows:

- `sourcedata`\
    Orignially collected MRI images in different formats packaged in zip and rar archives
- `sourcedata/code`\
    Code used to organize sourcedata into folders. Inputs for this code are not provided and it
    exists only for reference
- `rawdata`\
    MRI images converted to NIFTI and stored as
    [BIDS](https://bids.neuroimaging.io/)-like dataset. We don't provide the
    actual data files since they can be recovered with a pipeline in
    `rawdata/code`
- `rawdata/code`\
    Code used to convert sourcedata to BIDS format
- `rawdata/derivatives`\
    Derivative datasets for rawdata
- `rawdata/derivatives/fsf`\
    Freesurfer reconstruction pipeline
- `rawdata/derivatives/fsf/code`\
    Code for freesurfer reconstruction


Requirements
------------
- unix shell (cp, rm commands + possibility to install  unrar)
- anaconda\miniconda python installation
- docker for freesurfer cortical reconstruction

1. Download the code and change working directory to its root folder

    ```bash
    git clone https://github.com/dmalt/MRI_metacognition.git
    cd MRI_metacognition
    ```

2. Create and activate conda environment

    **On Linux** we recommend to install the complete environment snapshot with
    fixed package versions:
    ```bash
    conda env create -f environment_freeze.yml
    ```
    Alternatively,
    ```bash
    conda env create -f environment.yml
    ```
    can be used. It will install the latest package versions, but in this case
    something might break due to backward incompatibility.

    **On Windows** it's better to use the second option, which specifes only
    the primary dependencies and lets `conda` resolve the rest, since the
    secondary dependencies might be different between platforms.
    ```bash
    conda env create -f environment.yml
    ```

3. Install unrar and docker

    On Windows `unrar` installation might be problematic.
    There might be an option with pip/conda. In case `unrar` can't be installad,
    we recommend to unpack `.rar` archives and re-compress them as `.zip`

Launch
------
1. Get the data with
    ```bash
    dvc pull
    ```

    **Disclaimer**
    > The underlying GDrive data folder must be shared with you.
    > Otherwise you won't be able to download the data

2. Run the sourcedata-BIDS conversion pipeline from `rawdata/code`:
    ```bash
    doit
    ```

Adding new subjects
-------------------
To add a new subject, place the anatomy archive to `../../sourcedata/sub-<subject_id>/anat`
and run the first two pipeline steps:
```bash
doit unarchive
doit convert
```

Check `../sub-<subject_id>/anat` folder for the newly added subject. It should
have 2 files: `sub-<subject_id>_T1w.json` and `sub-<subject_id>_T1w.nii.gz`. If
these two files are present, it's all good. Run the whole pipeline again to
clean the temporary folders:

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
its `.nii.gz` file in one of the NIFTI viewers available
[online](https://socr.umich.edu/HTML5/BrainViewer/).

Once the correct series is found, open its `.json` file in a text editor and
find the `SeriesDescription` field. Use this field to append a section with a
new selection rule to the `dcm2bids_config.json` like this:

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

Usually "criteria" based only on "SeriesDescription" is enough, but in case
several files are selected you'll need to experiment with a more strict
criteria. For that, refer to the `dcm2bids`
[documentation](https://unfmontreal.github.io/Dcm2Bids/docs/how-to/create-config-file/)

**The second possibility** is that folders structure or data format inside the
subject's archive doesn't match that of other subjects. In this case such
subject requires special treatment.

To process this subject, open dodo.py and add an `if`-clause to `tast_convert`
in analogy to other corner-case subjects. To figure out an appropriate
`action`, look at the unarchived subject's files under `rawdata/tmp_dicom`.
Normally, this temporary folder is automatically deleted after the conversion,
but when something goes wrong and the pipeline doesn't finish, it should be
present. Another option would be to manually unarchive the subject in some temp
directory to check the folders structure.
