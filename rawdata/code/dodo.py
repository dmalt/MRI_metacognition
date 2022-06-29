import zipfile
from pathlib import Path
from shutil import copyfile, rmtree

import patoolib
from doit.tools import run_once

from config import src_dir, subjects, tmp_dicom_dir

DOIT_CONFIG = {"sort": "definition"}


def unzip(archive_path, dst_dir):
    with zipfile.ZipFile(archive_path, "r") as zip_ref:
        zip_ref.extractall(dst_dir)


def unrar(archive_path, dst_dir):
    patoolib.extract_archive(archive_path, outdir=dst_dir)


def mkdir(dirname):
    Path(dirname).mkdir(exist_ok=True, parents=True)


def task_unarchive():
    """Unarchive MRI data"""
    for s in subjects:
        data_dir = src_dir / f"sub-{s}" / "anat"
        path = next(data_dir.iterdir())
        dst_dir = tmp_dicom_dir / f"sub-{s}"
        # dst_dir.mkdir(exist_ok=True, parents=True)
        targ = dict(
            name=s,
            targets=[dst_dir],
            uptodate=[run_once],
        )
        targ["actions"] = [(mkdir, [dst_dir])]  # pyright: ignore
        if path.name.endswith(".zip"):
            targ["actions"].append((unzip, (path, dst_dir)))  # pyright: ignore
        elif path.name.endswith(".rar"):
            targ["actions"].append((unrar, (path, dst_dir)))  # pyright: ignore
        yield targ


def task_convert():
    """Convert to NIFTI format and copy to BIDS folders structure"""
    for s in subjects:
        task_dict = dict(
            name=s,
            targets=[
                f"../sub-{s}/anat/sub-{s}_T1w.nii.gz",
                f"../sub-{s}/anat/sub-{s}_T1w.json",
                f"../sub-{s}/anat",
                f"../sub-{s}",
            ],
            uptodate=[run_once],
            clean=True,
        )
        if s == "38":
            task_dict["actions"] = [  # pyright: ignore
                (mkdir, [f"../sub-{s}/anat"]),
                (
                    copyfile,
                    [
                        tmp_dicom_dir / f"sub-{s}/solev_ivan/3_3d_sag_t1_cube.nii.gz",
                        f"../sub-{s}/anat/sub-{s}_T1w.nii.gz",
                    ],
                ),
            ]
        elif s == "23":
            task_dict["actions"] = [
                (
                    f"dcm2bids -d {tmp_dicom_dir}/sub-{s}/Larionov/3D_DICOM"
                    + f" -c ./dcm2bids_config.json -p {s} -o ../"
                )
            ]
        else:
            task_dict["actions"] = [
                f"dcm2bids -d {tmp_dicom_dir}/sub-{s} -c ./dcm2bids_config.json -p {s} -o ../"
            ]
        yield task_dict


def task_clean_tmp_folders():
    """Remove temporary folders"""
    return dict(
        task_dep=["convert"],
        actions=[(rmtree, [f"{tmp_dicom_dir}"]), (rmtree, ["../tmp_dcm2bids"])],
    )


def create_participants_tsv():
    with open("../participants.tsv", "w") as f:
        f.write("\t".join(["participant_id", "name", "surname"]) + "\n")
        for s in subjects:
            data_dir = src_dir / f"sub-{s}" / "anat"
            surname, name = next(data_dir.iterdir()).stem.split("_")
            f.write("\t".join([f"sub-{s}", name.capitalize(), surname.capitalize()]) + "\n")


def task_create_participants_tsv():
    """Create tsv with participants subject id to name mapping"""
    return dict(
        actions=[create_participants_tsv],
        targets=["../participants.tsv"],
    )
