import json
import os
import cv2
import numpy as np


def load_labels(labels_path: str) -> list[str]:
    if not os.path.exists(labels_path):
        raise FileNotFoundError(f"Файл labels.json не найден: {labels_path}")

    with open(labels_path, "r", encoding="utf-8") as file:
        labels = json.load(file)

    if not isinstance(labels, list) or not labels:
        raise ValueError("labels.json должен содержать непустой список классов")

    return labels


def save_labels(labels: list[str], labels_path: str) -> None:
    with open(labels_path, "w", encoding="utf-8") as file:
        json.dump(labels, file, ensure_ascii=False, indent=2)


def preprocess_image(image_path: str, image_size: tuple[int, int]) -> np.ndarray:
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Не удалось открыть изображение")

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, image_size)
    image = image.astype("float32") / 255.0
    image = np.expand_dims(image, axis=0)

    return image