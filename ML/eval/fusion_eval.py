import argparse
from pathlib import Path
import yaml
import pandas as pd
from sklearn.metrics import accuracy_score, precision_recall_fscore_support


def load_cfg(path: str):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def load_preds(csv_path: Path):
    if not csv_path.exists():
        return None
    df = pd.read_csv(csv_path)
    return df


def evaluate(labels, probs):
    preds = [1 if p >= 0.5 else 0 for p in probs]
    acc = accuracy_score(labels, preds)
    p, r, f1, _ = precision_recall_fscore_support(labels, preds, average='binary', zero_division=0)
    return acc, p, r, f1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=True)
    args = ap.parse_args()

    cfg = load_cfg(args.config)
    paths = cfg['paths']
    fusion = cfg['fusion']

    preds_dir = Path(paths['preds_dir'])
    visual_csv = preds_dir / 'visual_preds.csv'
    audio_csv = preds_dir / 'audio_preds.csv'

    vis = load_preds(visual_csv)
    aud = load_preds(audio_csv)

    # Align by row order; in this baseline we rely on same test ordering
    if vis is None and aud is None:
        print('No predictions found. Run training scripts first.')
        return

    # Determine common evaluation length
    if vis is not None and aud is not None:
        n = min(len(vis), len(aud))
        visual_probs = vis['prob_fake'].tolist()[:n]
        audio_probs = aud['prob_fake'].tolist()[:n]
        # prefer visual labels for alignment; assume same order
        labels = vis['label'].tolist()[:n]
    elif vis is not None:
        visual_probs = vis['prob_fake'].tolist()
        audio_probs = [0.5] * len(vis)
        labels = vis['label'].tolist()
    else:  # aud is not None
        audio_probs = aud['prob_fake'].tolist()
        visual_probs = [0.5] * len(aud)
        labels = aud['label'].tolist()

    vw = float(fusion.get('visual_weight', 0.6))
    aw = float(fusion.get('audio_weight', 0.4))

    fused = [vw * v + aw * a for v, a in zip(visual_probs, audio_probs)]

    # Report metrics
    def report(name, probs):
        acc, p, r, f1 = evaluate(labels, probs)
        print(f"{name}: acc={acc:.4f} prec={p:.4f} rec={r:.4f} f1={f1:.4f}")

    if vis is not None:
        report('Visual', visual_probs)
    if aud is not None:
        report('Audio', audio_probs)
    report('Fused', fused)

    # Save fusion CSV
    out_csv = preds_dir / 'fused_preds.csv'
    pd.DataFrame({'prob_fake': fused, 'label': labels}).to_csv(out_csv, index=False)
    print(f"Wrote fused predictions to {out_csv}")


if __name__ == '__main__':
    main()
