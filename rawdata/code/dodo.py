from doit.tools import run_once

from config import src_dir, subjects, tmp_dicom_dir

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
        if s == "38":
            yield dict(
                name=s,
                actions=[
                    f"mkdir -p ../sub-{s}/anat",
                    f"cp {tmp_dicom_dir}/sub-{s}/*/*.nii.gz ../sub-{s}/anat/sub-{s}_T1w.nii.gz",
                ],
                targets=[f"../sub-{s}"],
                uptodate=[run_once],
            )
            continue
        elif s == "23":
            yield dict(
                name=s,
                actions=[
                    (
                        "dcm2bids -d"
                        f" {tmp_dicom_dir}/sub-{s}/Larionov/3D_DICOM -c"
                        f" ./dcm2bids_config.json -p {s} -o ../"
                    )
                ],
                targets=[f"../sub-{s}"],
                uptodate=[run_once],
            )
            continue
        yield dict(
            name=s,
            actions=[
                (
                    f"dcm2bids -d {tmp_dicom_dir}/sub-{s} -c"
                    f" ./dcm2bids_config.json -p {s} -o ../"
                )
            ],
            targets=[f"../sub-{s}"],
            uptodate=[run_once],
        )


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
