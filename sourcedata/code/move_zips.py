from pathlib import Path
from shutil import move

curdir = Path(".").resolve()
rootdir = (curdir / "..").resolve()

for i, archive in enumerate(sorted(rootdir.glob("*.*"))):
    subj_id = f"{i + 1:02}"
    # print(f"sub-{subj_id} --> ", archive)
    dst_dir = archive.parent / f"sub-{subj_id}" / "anat"
    dst_dir.mkdir(exist_ok=True, parents=True)
    dst = dst_dir / archive.name
    # print(dst)

    move(archive, dst)
