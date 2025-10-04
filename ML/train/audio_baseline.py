import argparse
from pathlib import Path
import yaml
import pandas as pd
import numpy as np
import librosa
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import accuracy_score


def load_cfg(path: str):
    with open(path, "r") as f:
        return yaml.safe_load(f)


class AudioDataset(Dataset):
    def __init__(self, audio_root: Path, split: str, sr: int = 16000, seconds: int = 5, n_mfcc: int = 40):
        self.items = []
        self.sr = sr
        self.seconds = seconds
        self.n_mfcc = n_mfcc
        for label_name, label in [("real", 0), ("fake", 1)]:
            base = audio_root / split / label_name
            if not base.exists():
                continue
            for wav in base.glob("*.wav"):
                self.items.append((wav, label))

    def __len__(self):
        return len(self.items)

    def __getitem__(self, idx):
        wav_path, label = self.items[idx]
        y, sr = librosa.load(wav_path, sr=self.sr, mono=True)
        target_len = self.seconds * self.sr
        if len(y) < target_len:
            y = np.pad(y, (0, target_len - len(y)))
        else:
            y = y[:target_len]
        # MFCC features [n_mfcc, T]
        mfcc = librosa.feature.mfcc(y=y, sr=self.sr, n_mfcc=self.n_mfcc)
        feat = torch.tensor(mfcc, dtype=torch.float32)  # [F, T]
        feat = feat.unsqueeze(0)  # [1, F, T]
        return feat, torch.tensor(label, dtype=torch.long)


class SmallAudioCNN(nn.Module):
    def __init__(self, n_mfcc: int = 40, n_classes: int = 2):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.AdaptiveAvgPool2d((1, 1))
        )
        self.head = nn.Linear(64, n_classes)
    
    def forward(self, x):  # x: [B,1,F,T]
        h = self.net(x)
        h = h.view(h.size(0), -1)
        return self.head(h)


def train_one_epoch(model, loader, criterion, optim, device):
    model.train()
    total = 0.0
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        optim.zero_grad()
        logits = model(x)
        loss = criterion(logits, y)
        loss.backward()
        optim.step()
        total += loss.item() * x.size(0)
    return total / len(loader.dataset)


def predict(model, loader, device):
    model.eval()
    probs, labels = [], []
    with torch.no_grad():
        for x, y in loader:
            x = x.to(device)
            logits = model(x)
            p = torch.softmax(logits, dim=-1)[:, 1].cpu().numpy()
            probs.extend(p.tolist())
            labels.extend(y.numpy().tolist())
    return probs, labels


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=True)
    ap.add_argument('--epochs', type=int, default=None)
    ap.add_argument('--batch-size', type=int, default=8)
    ap.add_argument('--lr', type=float, default=None)
    args = ap.parse_args()

    cfg = load_cfg(args.config)
    paths = cfg['paths']
    pp = cfg['preprocess']
    train_cfg = cfg['train']['audio']

    sr = pp.get('audio_sr', 16000)
    seconds = pp.get('audio_seconds', 5)
    n_mfcc = 40
    epochs = int(args.epochs or train_cfg.get('epochs', 2))
    lr = float(args.lr or train_cfg.get('lr', 5e-5))

    audio_root = Path(paths['extracted_audio_dir'])
    models_dir = Path(paths['models_dir']) / 'audio'
    preds_dir = Path(paths['preds_dir'])
    models_dir.mkdir(parents=True, exist_ok=True)
    preds_dir.mkdir(parents=True, exist_ok=True)

    train_ds = AudioDataset(audio_root, 'train', sr, seconds, n_mfcc)
    val_ds = AudioDataset(audio_root, 'val', sr, seconds, n_mfcc)
    test_ds = AudioDataset(audio_root, 'test', sr, seconds, n_mfcc)

    if len(train_ds) == 0:
        raise RuntimeError("No audio samples found. Ensure audio extraction created WAVs under extracted_audio_dir.")
    train_ld = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True, num_workers=2)
    val_ld = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False, num_workers=2)
    test_ld = DataLoader(test_ds, batch_size=args.batch_size, shuffle=False, num_workers=2)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = SmallAudioCNN(n_mfcc=n_mfcc).to(device)
    criterion = nn.CrossEntropyLoss()
    optim = torch.optim.Adam(model.parameters(), lr=lr)

    for ep in range(1, epochs + 1):
        tr_loss = train_one_epoch(model, train_ld, criterion, optim, device)
        val_probs, val_labels = predict(model, val_ld, device)
        val_pred = [1 if p >= 0.5 else 0 for p in val_probs]
        acc = accuracy_score(val_labels, val_pred)
        print(f"Epoch {ep}: train_loss={tr_loss:.4f} val_acc={acc:.4f}")

    ckpt = models_dir / 'audio_smallcnn.pt'
    torch.save(model.state_dict(), ckpt)
    print(f"Saved model to {ckpt}")

    test_probs, test_labels = predict(model, test_ld, device)
    out_csv = preds_dir / 'audio_preds.csv'
    pd.DataFrame({"prob_fake": test_probs, "label": test_labels}).to_csv(out_csv, index=False)
    print(f"Wrote predictions to {out_csv}")


if __name__ == '__main__':
    main()
