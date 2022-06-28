from config import src_dir, subjects, tmp_dicom_dir
from doit.tools import run_once

DOIT_CONFIG = {"sort": "definition"}


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
        targ["actions"] = [f"mkdir -p {dst_dir}"]
        if path.name.endswith(".zip"):
            targ["actions"].append(f"unzip {path} -d {dst_dir}")
        elif path.name.endswith(".rar"):
            targ["actions"].append(f"unrar x {path} {dst_dir}")
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
            task_dict["actions"] = [
                f"mkdir -p ../sub-{s}/anat",
                f"cp {tmp_dicom_dir}/sub-{s}/*/*.nii.gz ../sub-{s}/anat/sub-{s}_T1w.nii.gz",
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
        actions=[f"rm -rf {tmp_dicom_dir}", "rm -rf ../tmp_dcm2bids"],
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
