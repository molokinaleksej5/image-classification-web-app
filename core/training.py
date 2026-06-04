import os
import matplotlib.pyplot as plt
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam

from core.utils import save_labels


class ModelTrainer:
    def __init__(
        self,
        data_dir: str,
        model_path: str,
        labels_path: str,
        image_size: tuple[int, int] = (224, 224),
        batch_size: int = 32,
        epochs: int = 15
    ):
        self.data_dir = data_dir
        self.model_path = model_path
        self.labels_path = labels_path
        self.image_size = image_size
        self.batch_size = batch_size
        self.epochs = epochs

    def build_model(self, num_classes: int):
        base_model = MobileNetV2(
            input_shape=(self.image_size[0], self.image_size[1], 3),
            include_top=False,
            weights="imagenet"
        )
        base_model.trainable = False

        model = models.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.BatchNormalization(),
            layers.Dense(256, activation="relu"),
            layers.Dropout(0.35),
            layers.Dense(128, activation="relu"),
            layers.Dropout(0.25),
            layers.Dense(num_classes, activation="softmax")
        ])

        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss="categorical_crossentropy",
            metrics=["accuracy"]
        )
        return model

    def train(self):
        if not os.path.isdir(self.data_dir):
            raise FileNotFoundError(f"Папка датасета не найдена: {self.data_dir}")

        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)

        datagen = ImageDataGenerator(
            rescale=1.0 / 255.0,
            validation_split=0.2,
            rotation_range=20,
            zoom_range=0.2,
            width_shift_range=0.15,
            height_shift_range=0.15,
            shear_range=0.15,
            horizontal_flip=True,
            fill_mode="nearest"
        )

        train_generator = datagen.flow_from_directory(
            self.data_dir,
            target_size=self.image_size,
            batch_size=self.batch_size,
            class_mode="categorical",
            subset="training",
            shuffle=True
        )

        val_generator = datagen.flow_from_directory(
            self.data_dir,
            target_size=self.image_size,
            batch_size=self.batch_size,
            class_mode="categorical",
            subset="validation",
            shuffle=False
        )

        class_indices = train_generator.class_indices
        labels = [None] * len(class_indices)

        for class_name, class_id in class_indices.items():
            labels[class_id] = class_name

        save_labels(labels, self.labels_path)

        model = self.build_model(num_classes=len(labels))

        callbacks = [
            EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True),
            ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=2),
            ModelCheckpoint(self.model_path, monitor="val_accuracy", save_best_only=True)
        ]

        history = model.fit(
            train_generator,
            validation_data=val_generator,
            epochs=self.epochs,
            callbacks=callbacks
        )

        self.plot_history(history)
        return history

    @staticmethod
    def plot_history(history):
        acc = history.history["accuracy"]
        val_acc = history.history["val_accuracy"]
        loss = history.history["loss"]
        val_loss = history.history["val_loss"]
        epochs_range = range(1, len(acc) + 1)

        plt.figure(figsize=(10, 5))
        plt.plot(epochs_range, acc, label="Точность обучения")
        plt.plot(epochs_range, val_acc, label="Точность валидации")
        plt.title("График точности модели")
        plt.xlabel("Эпоха")
        plt.ylabel("Accuracy")
        plt.legend()
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(10, 5))
        plt.plot(epochs_range, loss, label="Потери обучения")
        plt.plot(epochs_range, val_loss, label="Потери валидации")
        plt.title("График функции потерь")
        plt.xlabel("Эпоха")
        plt.ylabel("Loss")
        plt.legend()
        plt.tight_layout()
        plt.show()