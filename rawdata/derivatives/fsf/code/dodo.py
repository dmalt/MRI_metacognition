import json
import os

from doit.tools import run_once

import config


def create_dset_description():
    json_dict = {
        "Name": config.pipeline_name,
        "BidsVersion": config.bids_version,
        "Authors": config.authors,
        "DatasetType": "derivative",
        "GeneratedBy": [
            {
                "Name": "MRI_metacognition",
                "CodeUrl": config.code_url,
                "Container": {
                    "Type": "docker",
                    "Tag": config.docker_tagged_image,
                    "URI": config.docker_url,
                },
            }
        ],
    }
    with (config.root / "dataset_description.json").open("w") as f:
        json.dump(json_dict, f, indent=4)
    print(json_dict)


def task_create_dataset_description():
    return {
        "uptodate": [run_once],
        "targets": [config.root / "dataset_description.json"],
        "actions": [create_dset_description],
    }


def task_pipeline():
    for subj in config.subjects:
        anat_dir = config.src_dir / f"sub-{subj}" / "anat"
        anat_file = f"sub-{subj}_T1w.nii.gz"
        yield dict(
            name=f"sub-{subj}",
            file_dep=[anat_dir / anat_file],
            actions=[
                f"{config.docker_base} -v {anat_dir}:/anat "
                + f"{config.docker_tagged_image} "
                + f"subject=sub-{subj} "
                + f'recon_all_cmd="-i /anat/{anat_file} -all" --verbosity 2'
            ],
            targets=[config.root / f"sub-{subj}"],
        )
