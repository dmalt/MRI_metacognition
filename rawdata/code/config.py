from pathlib import Path

root = Path("..").resolve()
tmp_dicom_dir = root / "tmp_dicom"
src_dir = root / ".." / "sourcedata"

n_subj = len(list(filter(lambda x: x.is_dir(), src_dir.glob("sub-*"))))
all_subjects = sorted(str(i + 1).zfill(2) for i in range(n_subj))
bad_subjects = ["41"]  # weird MRI: very few slices in each of 3 sequences
subjects = [s for s in all_subjects if s not in bad_subjects]
