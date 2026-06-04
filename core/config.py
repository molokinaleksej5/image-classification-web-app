import os


class Config:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
    MODEL_DIR = os.path.join(BASE_DIR, "model")
    DATASET_DIR = os.path.join(BASE_DIR, "dataset")
    MODEL_PATH = os.path.join(MODEL_DIR, "best_model.keras")
    LABELS_PATH = os.path.join(BASE_DIR, "labels.json")
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

    IMAGE_SIZE = (224, 224)
    MAX_CONTENT_LENGTH = 15 * 1024 * 1024
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp", "webp"}

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(INSTANCE_DIR, 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "intel-image-ai-secret-key"

    CLASS_TRANSLATIONS = {
        "buildings": "Здания",
        "forest": "Лес",
        "glacier": "Ледник",
        "mountain": "Горы",
        "sea": "Море",
        "street": "Улица"
    }