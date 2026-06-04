import argparse
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.training import ModelTrainer
from core.config import Config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, default=Config.DATASET_DIR)
    parser.add_argument("--epochs", type=int, default=15)
    parser.add_argument("--batch_size", type=int, default=32)
    args = parser.parse_args()

    trainer = ModelTrainer(
        data_dir=args.data_dir,
        model_path=Config.MODEL_PATH,
        labels_path=Config.LABELS_PATH,
        image_size=Config.IMAGE_SIZE,
        batch_size=args.batch_size,
        epochs=args.epochs
    )
    trainer.train()


if __name__ == "__main__":
    main()