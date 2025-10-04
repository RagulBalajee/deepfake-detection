import argparse
import os
from pathlib import Path
import yaml
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
from sklearn.metrics import accuracy_score, precision_recall_fscore_support


def load_cfg(path: str):
    with open(path, "r") as f:
        return yaml.safe_load(f)


class FrameDataset(Dataset):
    def __init__(self, frames_root: Path, split: str, transform=None):
        self.samples = []
        self.transform = transform
        # Expect structure: frames_root/split/{real|fake}/{video_id}/frame_*.jpg
        for label_name, label in [("real", 0), ("fake", 1)]:
            base = frames_root / split / label_name
            if not base.exists():
                continue
            for vid_dir in base.iterdir():
                if not vid_dir.is_dir():
                    continue
                # Pick first available frame
                imgs = sorted(list(vid_dir.glob("*.jpg")))
                if not imgs:
                    continue
                self.samples.append((imgs[0], label))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img_path, label = self.samples[idx]
        img = Image.open(img_path).convert("RGB")
        if self.transform:
            img = self.transform(img)
        return img, torch.tensor(label, dtype=torch.long)


def build_model(num_classes=2):
    # Lightweight ResNet18 without pretrained weights (offline friendly)
    from torchvision.models import resnet18
    model = resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    return model


def train_one_epoch(model, loader, criterion, optim, device):
    model.train()
    total_loss = 0.0
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        optim.zero_grad()
        logits = model(x)
        loss = criterion(logits, y)
        loss.backward()
        optim.step()
        total_loss += loss.item() * x.size(0)
    return total_loss / len(loader.dataset)


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
    ap.add_argument("--config", required=True)
    ap.add_argument("--epochs", type=int, default=None)
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--lr", type=float, default=None)
    args = ap.parse_args()

    cfg = load_cfg(args.config)
    paths = cfg["paths"]
    train_cfg = cfg["train"]["visual"]
    epochs = int(args.epochs or train_cfg.get("epochs", 3))
    lr = float(args.lr or train_cfg.get("lr", 3e-4))
    image_size = train_cfg.get("image_size", 224)

    frames_root = Path(paths["extracted_frames_dir"]) 
    models_dir = Path(paths["models_dir"]) / "visual"
    preds_dir = Path(paths["preds_dir"]) 
    models_dir.mkdir(parents=True, exist_ok=True)
    preds_dir.mkdir(parents=True, exist_ok=True)

    transform = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    train_ds = FrameDataset(frames_root, "train", transform)
    val_ds = FrameDataset(frames_root, "val", transform)
    test_ds = FrameDataset(frames_root, "test", transform)

    train_ld = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True, num_workers=2)
    val_ld = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False, num_workers=2)
    test_ld = DataLoader(test_ds, batch_size=args.batch_size, shuffle=False, num_workers=2)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = build_model().to(device)
    criterion = nn.CrossEntropyLoss()
    optim = torch.optim.Adam(model.parameters(), lr=lr)

    for ep in range(1, epochs + 1):
        tr_loss = train_one_epoch(model, train_ld, criterion, optim, device)
        val_probs, val_labels = predict(model, val_ld, device)
        val_pred = [1 if p >= 0.5 else 0 for p in val_probs]
        acc = accuracy_score(val_labels, val_pred)
        print(f"Epoch {ep}: train_loss={tr_loss:.4f} val_acc={acc:.4f}")

    # Save
    ckpt = models_dir / "visual_resnet18.pt"
    torch.save(model.state_dict(), ckpt)
    print(f"Saved model to {ckpt}")

    # Predict test and store CSV
    test_probs, test_labels = predict(model, test_ld, device)
    out_csv = preds_dir / "visual_preds.csv"
    pd.DataFrame({"prob_fake": test_probs, "label": test_labels}).to_csv(out_csv, index=False)
    print(f"Wrote predictions to {out_csv}")


if __name__ == "__main__":
    main()
