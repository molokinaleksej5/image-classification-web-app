# Image Classification Web App

![Python](https://img.shields.io/badge/Python-3.11-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-Keras-orange)
![MobileNetV2](https://img.shields.io/badge/Model-MobileNetV2-green)
![Flask](https://img.shields.io/badge/Flask-Web%20App-black)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![License](https://img.shields.io/badge/License-MIT-blue)

Веб-приложение для классификации изображений с использованием нейронной сети MobileNetV2, TensorFlow/Keras и Flask.

Проект решает задачу многоклассовой классификации природных и городских сцен. Пользователь загружает изображение через веб-интерфейс, система выполняет предсказание, показывает итоговый класс, уверенность модели и вероятности по всем категориям.

---

## О проекте
В проекте реализованы:

* обучение модели классификации изображений;
* использование MobileNetV2 с transfer learning;
* загрузка изображений через Flask-интерфейс;
* проверка допустимых форматов файлов;
* предварительная обработка изображения;
* вывод предсказанного класса;
* отображение уверенности модели;
* вывод топ-предсказаний;
* сохранение истории классификаций;
* страница статистики;
* хранение результатов в SQLite;
* формирование отчётов с метриками качества.

---

## Классы изображений

Модель классифицирует изображение по 6 категориям:

| Класс     | Русское название |
| --------- | ---------------- |
| buildings | Здания           |
| forest    | Лес              |
| glacier   | Ледник           |
| mountain  | Горы             |
| sea       | Море             |
| street    | Улица            |

---

## Архитектура модели

В проекте используется MobileNetV2, предварительно обученная на ImageNet.

Базовая часть MobileNetV2 используется как экстрактор признаков. Поверх неё добавлена собственная классификационная голова для 6 классов.

Параметры обучения:

| Параметр         |                 Значение |
| ---------------- | -----------------------: |
| Image size       |                  224×224 |
| Batch size       |                       32 |
| Epochs           |                       15 |
| Optimizer        |                     Adam |
| Learning rate    |                    0.001 |
| Loss             | Categorical Crossentropy |
| Validation split |                      20% |

Для повышения устойчивости модели использовалась аугментация данных:

* повороты;
* масштабирование;
* сдвиги по ширине и высоте;
* shear-преобразования;
* горизонтальное отражение;
* нормализация пикселей.

---

## Результаты модели

Модель была оценена на выборке из 13 097 изображений.

Итоговые метрики:

| Метрика            | Значение |
| ------------------ | -------: |
| Accuracy           |   0.9282 |
| Top-2 Accuracy     |   0.9917 |
| Top-3 Accuracy     |   0.9980 |
| Macro Precision    |   0.9223 |
| Macro Recall       |   0.9248 |
| Macro F1-score     |   0.9231 |
| Weighted Precision |   0.9296 |
| Weighted Recall    |   0.9282 |
| Weighted F1-score  |   0.9285 |

Общая точность модели составила **92.82%**.
---

## Метрики по классам

| Класс     | Precision | Recall | F1-score | Support |
| --------- | --------: | -----: | -------: | ------: |
| buildings |    0.9568 | 0.9087 |   0.9321 |    2191 |
| forest    |    0.9925 | 0.9912 |   0.9918 |    2271 |
| glacier   |    0.7943 | 0.8609 |   0.8263 |    1467 |
| mountain  |    0.9011 | 0.8670 |   0.8837 |    2512 |
| sea       |    0.9666 | 0.9556 |   0.9611 |    2274 |
| street    |    0.9226 | 0.9656 |   0.9436 |    2382 |

Лучше всего модель распознаёт классы `forest`, `sea`, `street` и `buildings`. Более сложными являются классы `glacier` и `mountain`, так как изображения ледников и гор часто визуально похожи по цвету, текстуре и структуре сцены.

---

## Используемые технологии

### Machine Learning

* Python
* TensorFlow
* Keras
* MobileNetV2
* NumPy
* Pandas
* Scikit-learn

### Web

* Flask
* Flask-SQLAlchemy
* HTML
* CSS
* JavaScript

### Database

* SQLite

### Computer Vision

* PIL
* OpenCV

### Отчёты и анализ

* Matplotlib
* CSV reports
* JSON metrics

---

## Автор

**Алексей Молокин**
ML Engineer / Python Developer

GitHub: [molokinaleksej5](https://github.com/molokinaleksej5)
