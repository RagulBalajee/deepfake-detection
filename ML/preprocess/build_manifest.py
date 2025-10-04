import argparse
import os
import random
import pandas as pd
import yaml
from pathlib import Path


VIDEO_EXTS = {'.mp4', '.mov', '.avi', '.mkv', '.webm'}


def gather_items(root: Path, media_type: str, dataset_name: str):
    items = []
    for label in ["real", "fake"]:
        base = root / label
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.is_file():
                ext = p.suffix.lower()
                if media_type == "video" and ext in VIDEO_EXTS:
                    items.append({
                        "path": str(p),
                        "label": 0 if label == "real" else 1,
                        "type": media_type,
                        "dataset": dataset_name,
                    })
    return items


def load_cfg(path: str):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()

    cfg = load_cfg(args.config)
    paths = cfg["paths"]
    splits = cfg["splits"]

    out_dir = Path(paths["manifests_dir"]).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    # Prefer new generic dataset list if present
    datasets = paths.get("datasets")
    if datasets:
        for ds in datasets:
            root = Path(ds.get("root", "")).expanduser()
            name = ds.get("name", "unknown")
            rows += gather_items(root, "video", name)
    else:
        # Fallback to legacy keys
        dfdc_root = Path(paths["dfdc_root"]).expanduser()
        hav_root = Path(paths["havdf_root"]).expanduser()
        rows += gather_items(dfdc_root, "video", "DFDC")
        rows += gather_items(hav_root, "video", "HAVDF")

    random.seed(splits.get("seed", 42))
    random.shuffle(rows)

    n = len(rows)
    n_train = int(n * splits.get("train_ratio", 0.7))
    n_val = int(n * splits.get("val_ratio", 0.15))

    for i, r in enumerate(rows):
        if i < n_train:
            r["split"] = "train"
        elif i < n_train + n_val:
            r["split"] = "val"
        else:
            r["split"] = "test"

    df = pd.DataFrame(rows)
    out_csv = out_dir / "manifest.csv"
    df.to_csv(out_csv, index=False)
    print(f"Wrote manifest: {out_csv} ({len(df)} rows)")


if __name__ == "__main__":
    main()
