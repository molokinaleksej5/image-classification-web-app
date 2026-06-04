import os
import json
from tensorflow.keras.models import load_model

from core.config import Config
from core.utils import load_labels, preprocess_image


class ImagePredictor:
    def __init__(self, model_path: str, labels_path: str, image_size: tuple[int, int]):
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Модель не найдена: {model_path}. Сначала обучите модель на Intel Image Classification."
            )

        self.model = load_model(model_path)
        self.labels = load_labels(labels_path)
        self.image_size = image_size
        self.allowed_extensions = Config.ALLOWED_EXTENSIONS
        self.class_translations = Config.CLASS_TRANSLATIONS

    def allowed_file(self, filename: str) -> bool:
        return "." in filename and filename.rsplit(".", 1)[1].lower() in self.allowed_extensions

    def predict(self, image_path: str) -> dict:
        image = preprocess_image(image_path, self.image_size)
        predictions = self.model.predict(image, verbose=0)[0]

        indexed = []
        for idx, prob in enumerate(predictions):
            class_en = self.labels[idx]
            indexed.append({
                "class": class_en,
                "class_ru": self.class_translations.get(class_en, class_en),
                "probability": round(float(prob * 100), 2)
            })

        indexed.sort(key=lambda x: x["probability"], reverse=True)

        predicted_class = indexed[0]["class"]
        predicted_class_ru = indexed[0]["class_ru"]
        confidence = indexed[0]["probability"]

        return {
            "predicted_class": predicted_class,
            "predicted_class_ru": predicted_class_ru,
            "confidence": confidence,
            "top_predictions": indexed[:6],
            "top_predictions_ru": indexed[:6],
            "probabilities_json": json.dumps(indexed, ensure_ascii=False)
        }