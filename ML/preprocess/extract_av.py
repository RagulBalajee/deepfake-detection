import argparse
import os
import cv2
import pandas as pd
import numpy as np
import librosa
import soundfile as sf
from pathlib import Path
import yaml
import ffmpeg


def load_cfg(path: str):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def extract_frames(video_path: str, out_dir: Path, num_frames: int, fps: int):
    ensure_dir(out_dir)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return 0
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    orig_fps = cap.get(cv2.CAP_PROP_FPS) or fps
    if total <= 0:
        # fallback: sample first num_frames
        idxs = list(range(num_frames))
    else:
        step = max(int((orig_fps // fps) if orig_fps >= fps and fps > 0 else max(total // max(num_frames,1), 1)), 1)
        idxs = list(range(0, min(total, step * num_frames), step))[:num_frames]
    saved = 0
    for i, idx in enumerate(idxs):
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ok, frame = cap.read()
        if not ok:
            continue
        out_fp = out_dir / f"frame_{i:04d}.jpg"
        cv2.imwrite(str(out_fp), frame)
        saved += 1
    cap.release()
    return saved


def extract_audio_ffmpeg(video_path: str, out_wav: Path, sr: int, seconds: int):
    ensure_dir(out_wav.parent)
    try:
        (
            ffmpeg
            .input(video_path)
            .output(str(out_wav), format='wav', acodec='pcm_s16le', ac=1, ar=sr, t=seconds)
            .overwrite_output()
            .run(quiet=True)
        )
        return True
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=True)
    ap.add_argument('--num-frames', type=int, default=None)
    ap.add_argument('--fps', type=int, default=None)
    args = ap.parse_args()

    cfg = load_cfg(args.config)
    paths = cfg['paths']
    pp = cfg['preprocess']
    num_frames = args.num_frames or pp.get('frames_per_video', 16)
    fps = args.fps or pp.get('fps', 4)
    audio_sr = pp.get('audio_sr', 16000)
    audio_seconds = pp.get('audio_seconds', 5)

    manifest_csv = Path(paths['manifests_dir']) / 'manifest.csv'
    df = pd.read_csv(manifest_csv)

    frames_root = Path(paths['extracted_frames_dir'])
    audio_root = Path(paths['extracted_audio_dir'])
    ensure_dir(frames_root); ensure_dir(audio_root)

    stats = {"frames": 0, "audio": 0}

    for _, row in df.iterrows():
        vp = Path(row['path'])
        split = row['split']
        label = 'real' if int(row['label']) == 0 else 'fake'
        vid_key = vp.stem

        # Frames
        out_frames_dir = frames_root / split / label / vid_key
        saved = extract_frames(str(vp), out_frames_dir, num_frames, fps)
        stats['frames'] += saved

        # Audio (best-effort)
        out_wav = audio_root / split / label / f"{vid_key}.wav"
        ok = extract_audio_ffmpeg(str(vp), out_wav, audio_sr, audio_seconds)
        if not ok:
            # fallback: use sibling .wav with same stem if exists
            sib_wav = vp.with_suffix('.wav')
            if sib_wav.exists():
                ensure_dir(out_wav.parent)
                try:
                    import shutil
                    shutil.copyfile(sib_wav, out_wav)
                    ok = True
                except Exception:
                    ok = False
        if ok:
            stats['audio'] += 1

    print(f"Done. Saved frames: {stats['frames']} | audio clips: {stats['audio']}")


if __name__ == '__main__':
    main()
