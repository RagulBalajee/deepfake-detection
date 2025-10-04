# Fake News & Deepfake Detection – ML Pipeline

This folder contains a lightweight end‑to‑end pipeline to prepare DFDC (subset) and HAV‑DF (subset), preprocess data, train baselines, and evaluate/fuse results.

## Folder layout
- `configs/config.yaml` – central paths and knobs.
- `scripts/download_subsets.py` – helper to place/verify dataset subsets.
- `preprocess/build_manifest.py` – scans datasets and produces CSV manifests.
- `preprocess/extract_av.py` – extracts frames and audio (FFmpeg / librosa).
- `train/visual_baseline.py` – frame‑level visual baseline (timm EfficientNet‑B0).
- `train/audio_baseline.py` – audio baseline (Wav2Vec2 fine‑tune).
- `train/video_seq_baseline.py` – 3D‑CNN + LSTM scaffold (optional/advanced).
- `eval/fusion_eval.py` – late‑fusion of model outputs and metrics.

## Quickstart
1) Install deps (new venv recommended):
```bash
pip install -r requirements-ml.txt
```

2) Configure paths in `ML/configs/config.yaml` (edit dataset locations).

3) Build manifests (CSV with `path,label,split,type`):
```bash
python ML/preprocess/build_manifest.py --config ML/configs/config.yaml
```

4) Extract frames and audio (uses FFmpeg if available, falls back to librosa for audio):
```bash
python ML/preprocess/extract_av.py --config ML/configs/config.yaml --num-frames 16 --fps 4
```

5) Train visual baseline on extracted frames:
```bash
python ML/train/visual_baseline.py --config ML/configs/config.yaml --epochs 3 --batch-size 32
```

6) Train audio baseline on extracted audio clips:
```bash
python ML/train/audio_baseline.py --config ML/configs/config.yaml --epochs 2 --batch-size 8
```

7) Evaluate + fuse predictions:
```bash
python ML/eval/fusion_eval.py --config ML/configs/config.yaml
```

## Notes
- This pipeline is subset‑friendly (~4–5 GB). You control the exact subset size by which files you place under the dataset folders.
- Video URL ingestion is out of scope here; place local files in the dataset roots defined below.
- Visual/audio models are baselines to get you started and are easily swappable.
