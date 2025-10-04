import argparse
from pathlib import Path
import cv2
import numpy as np
import soundfile as sf
import os

"""
Generate a tiny synthetic AV dataset for smoke testing the pipeline.
Creates a few short videos with simple moving shapes and a mono sine tone.
"""

def make_video(out_path: Path, kind: str, seconds: int = 3, fps: int = 12, size=(320, 240)):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    vw = cv2.VideoWriter(str(out_path), fourcc, fps, size)
    W, H = size
    n_frames = seconds * fps
    for i in range(n_frames):
        img = np.zeros((H, W, 3), dtype=np.uint8)
        # 'real' draw a circle; 'fake' draw a rectangle with jitter
        if kind == 'real':
            cx = int(W/2 + (W/4) * np.sin(2*np.pi*i/n_frames))
            cy = int(H/2)
            cv2.circle(img, (cx, cy), 30, (0, 255, 0), -1)
        else:
            x = int(W/2 + (W/4) * np.sin(2*np.pi*i/n_frames))
            y = int(H/2 + 10*np.sin(2*np.pi*i/12))  # jitter to mimic artifact
            cv2.rectangle(img, (x-30, y-20), (x+30, y+20), (0, 0, 255), -1)
            # add slight blocky artifact
            if i % 3 == 0:
                cv2.putText(img, 'DF', (5, H-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
        vw.write(img)
    vw.release()


def make_audio_wav(out_wav: Path, kind: str, seconds: int = 3, sr: int = 16000):
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    t = np.linspace(0, seconds, int(sr*seconds), endpoint=False)
    # base sine tone; fake has added tremolo to imitate manipulation
    base_freq = 440.0
    tone = 0.2 * np.sin(2*np.pi*base_freq*t)
    if kind == 'fake':
        mod = (1.0 + 0.4*np.sin(2*np.pi*3*t))
        tone = tone * mod
    sf.write(str(out_wav), tone.astype(np.float32), sr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dfdc', default='data/DFDC_subset')
    ap.add_argument('--havdf', default='data/HAVDF_subset')
    ap.add_argument('--count', type=int, default=5, help='videos per class per dataset')
    args = ap.parse_args()

    for dataset_root in [args.dfdc, args.havdf]:
        for label in ['real', 'fake']:
            root = Path(dataset_root)/label
            root.mkdir(parents=True, exist_ok=True)
            for i in range(args.count):
                vid = root / f'sample_{i:02d}.mp4'
                make_video(vid, label)
                # also drop a wav with same stem for HAVDF realism; not required by pipeline but useful
                wav = root / f'sample_{i:02d}.wav'
                make_audio_wav(wav, label)
    print('Synthetic dataset generated.')

if __name__ == '__main__':
    main()
