import argparse
from pathlib import Path
import shutil

"""
This helper does not download large datasets. It verifies that the subset
folders exist and shows a quick summary. Place your subset files here:
- data/DFDC_subset/{real,fake}/*.mp4
- data/HAVDF_subset/{real,fake}/*.mp4
You can symlink or copy from your storage.
"""

def summarize(root: Path):
    if not root.exists():
        return {"exists": False, "count": 0}
    files = list(root.rglob("*.mp4")) + list(root.rglob("*.mov")) + list(root.rglob("*.avi")) + list(root.rglob("*.mkv"))
    return {"exists": True, "count": len(files)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dfdc", default="data/DFDC_subset")
    ap.add_argument("--havdf", default="data/HAVDF_subset")
    args = ap.parse_args()

    dfdc = Path(args.dfdc)
    hav = Path(args.havdf)

    print("Checking dataset roots...")
    dfdc_s = summarize(dfdc)
    hav_s = summarize(hav)

    print(f"DFDC_subset: exists={dfdc_s['exists']} videos={dfdc_s['count']}")
    print(f"HAVDF_subset: exists={hav_s['exists']} videos={hav_s['count']}")

    if not dfdc_s['exists']:
        print(f"Create folders: {dfdc/'real'} and {dfdc/'fake'} and place ~50-100 videos.")
    if not hav_s['exists']:
        print(f"Create folders: {hav/'real'} and {hav/'fake'} and place ~100 videos.")


if __name__ == "__main__":
    main()
