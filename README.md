Convert ../../sourcedata to BIDS format. Convert DICOM to NIFTI on the way.

Requirements
------------
- unix shell (cp, rm commands + possibility to install unzip and unrar)
- anaconda\miniconda python installation

Installation
------------
1. Create and activate conda environment
```bash
conda env create -f environment.yml
conda activate mri
```
2. Install unzip and unrar

Launch
------
To run the conversion pipeline, execute
```bash
doit
```
