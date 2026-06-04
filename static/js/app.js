const form = document.getElementById("upload-form");
const input = document.getElementById("image-input");
const dropZone = document.getElementById("drop-zone");
const previewImage = document.getElementById("preview-image");
const previewPlaceholder = document.getElementById("preview-placeholder");
const resultSection = document.getElementById("result-section");
const resultImage = document.getElementById("result-image");
const predictedClass = document.getElementById("predicted-class");
const confidence = document.getElementById("confidence");
const probabilitiesList = document.getElementById("probabilities-list");
const statusMessage = document.getElementById("status-message");

if (dropZone) {
    dropZone.addEventListener("click", () => input.click());

    input.addEventListener("change", () => {
        if (input.files.length > 0) {
            showPreview(input.files[0]);
        }
    });

    dropZone.addEventListener("dragover", (event) => {
        event.preventDefault();
        dropZone.classList.add("dragover");
    });

    dropZone.addEventListener("dragleave", () => {
        dropZone.classList.remove("dragover");
    });

    dropZone.addEventListener("drop", (event) => {
        event.preventDefault();
        dropZone.classList.remove("dragover");

        const files = event.dataTransfer.files;
        if (files.length > 0) {
            input.files = files;
            showPreview(files[0]);
        }
    });
}

function showPreview(file) {
    const reader = new FileReader();
    reader.onload = function (event) {
        previewImage.src = event.target.result;
        previewImage.classList.remove("hidden");
        previewPlaceholder.classList.add("hidden");
    };
    reader.readAsDataURL(file);
}

if (form) {
    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        if (!input.files.length) {
            setStatus("Сначала выберите изображение", true);
            return;
        }

        const formData = new FormData();
        formData.append("image", input.files[0]);

        setStatus("Выполняется анализ изображения...", false);

        try {
            const response = await fetch("/predict", {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                setStatus(data.error || "Ошибка обработки", true);
                return;
            }

            setStatus("Классификация успешно завершена", false);
            renderResult(data);
        } catch (error) {
            setStatus("Не удалось отправить запрос на сервер", true);
        }
    });
}

function setStatus(message, isError) {
    statusMessage.textContent = message;
    statusMessage.className = isError ? "status-message error" : "status-message success";
}

function renderResult(data) {
    resultSection.classList.remove("hidden");
    resultImage.src = data.image_url;
    predictedClass.textContent = data.predicted_class;
    confidence.textContent = `${data.confidence}%`;

    probabilitiesList.innerHTML = "";

    data.top_predictions.forEach(item => {
        const row = document.createElement("div");
        row.className = "prob-row";

        row.innerHTML = `
            <div class="prob-head">
                <span>${item.class_ru}</span>
                <span>${item.probability}%</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width:${item.probability}%"></div>
            </div>
        `;

        probabilitiesList.appendChild(row);
    });

    resultSection.scrollIntoView({ behavior: "smooth" });
}