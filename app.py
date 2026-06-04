import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, url_for, redirect
from werkzeug.utils import secure_filename

from core.config import Config
from core.database import db
from core.models import PredictionHistory
from core.predictor import ImagePredictor

app = Flask(__name__)
app.config.from_object(Config)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["INSTANCE_DIR"], exist_ok=True)
os.makedirs(app.config["MODEL_DIR"], exist_ok=True)

db.init_app(app)

with app.app_context():
    db.create_all()

predictor = ImagePredictor(
    model_path=app.config["MODEL_PATH"],
    labels_path=app.config["LABELS_PATH"],
    image_size=app.config["IMAGE_SIZE"]
)


@app.route("/")
def index():
    recent_items = PredictionHistory.query.order_by(PredictionHistory.created_at.desc()).limit(6).all()
    total_predictions = PredictionHistory.query.count()
    return render_template("index.html", recent_items=recent_items, total_predictions=total_predictions)


@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "Файл не найден"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "Файл не выбран"}), 400

    if not predictor.allowed_file(file.filename):
        return jsonify({"error": "Недопустимый формат файла"}), 400

    original_name = secure_filename(file.filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"{timestamp}_{original_name}"
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(save_path)

    try:
        result = predictor.predict(save_path)
        image_url = url_for("static", filename=f"uploads/{filename}")

        record = PredictionHistory(
            filename=filename,
            predicted_class=result["predicted_class"],
            confidence=result["confidence"],
            probabilities_json=result["probabilities_json"]
        )
        db.session.add(record)
        db.session.commit()

        return jsonify({
            "filename": filename,
            "image_url": image_url,
            "predicted_class": result["predicted_class_ru"],
            "predicted_class_en": result["predicted_class"],
            "confidence": result["confidence"],
            "top_predictions": result["top_predictions_ru"]
        })
    except Exception as exc:
        return jsonify({"error": f"Ошибка обработки: {str(exc)}"}), 500


@app.route("/history")
def history():
    items = PredictionHistory.query.order_by(PredictionHistory.created_at.desc()).all()
    return render_template("history.html", items=items)


@app.route("/stats")
def stats():
    total = PredictionHistory.query.count()
    all_items = PredictionHistory.query.order_by(PredictionHistory.created_at.desc()).all()

    class_counts = {}
    avg_confidence = 0.0

    for item in all_items:
        class_counts[item.predicted_class] = class_counts.get(item.predicted_class, 0) + 1
        avg_confidence += item.confidence

    avg_confidence = round(avg_confidence / total, 2) if total else 0.0

    class_map = Config.CLASS_TRANSLATIONS
    chart_labels = [class_map.get(name, name) for name in class_counts.keys()]
    chart_values = list(class_counts.values())
    latest_items = all_items[:10]

    return render_template(
        "stats.html",
        total=total,
        avg_confidence=avg_confidence,
        chart_labels=chart_labels,
        chart_values=chart_values,
        latest_items=latest_items,
        class_map=class_map
    )


@app.route("/delete-history", methods=["POST"])
def delete_history():
    items = PredictionHistory.query.all()
    for item in items:
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], item.filename)
        if os.path.exists(file_path):
            os.remove(file_path)

    PredictionHistory.query.delete()
    db.session.commit()
    return redirect(url_for("history"))


if __name__ == "__main__":
    app.run(debug=True)