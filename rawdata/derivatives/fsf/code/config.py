import os
from pathlib import Path

root = Path("..").resolve()
src_dir = (root / ".." / "..").resolve()

n_subj = len(list(src_dir.glob("sub-*")))
all_subjects = sorted(str(i + 1).zfill(2) for i in range(n_subj))
bad_subjects = ["41"]  # weird MRI: very few slices in each of 3 sequences
subjects = [s for s in all_subjects if s not in bad_subjects]


pipeline_name = "fsf"
bids_version = "1.6.0"
authors = ["Dmitrii Altukhov", "Maria Alekseeva", "Beatriz Martin-Luengo"]
code_url = "https://github.com/dmalt/MRI_metacognition/blob/main/rawdata/code/dodo.py"

docker_subj_dir = "/subjects"
docker_image = "dmalt/freesurfer"
docker_tag = "7.1.1"
docker_url = "https://hub.docker.com/repository/docker/dmalt/freesurfer"
docker_tagged_image = docker_image + ":" + docker_tag

try:
    pass_uid = f"-e LOCAL_USER_ID={os.getuid()}"
except AttributeError:
    pass_uid = ""

docker_base = f"docker run --rm -v {root}/:{docker_subj_dir} {pass_uid}"


if __name__ == "__main__":
    print(f"{src_dir=}, {n_subj=}")
