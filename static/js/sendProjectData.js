document.addEventListener("DOMContentLoaded", () => {
  const btnSaveData = document.getElementById("generator-btn");
  const loading = document.getElementById("loading-animation");
  const card = document.getElementById("card");
  let defaultTariff;
  let premiumTariff;

  btnSaveData.addEventListener("click", () => {
    // Запрос в бд, для получение баланса
    fetch("/get_tariff_data")
      .then((response) => response.json())
      .then((data) => {
        console.log("Tariff data:", data);

        defaultTariff = data.defaultTariff;
        premiumTariff = data.premiumTariff;
        console.log("Tariff data:", data.defaultTariff, data.premiumTariff);
      })
      .catch((error) => {
        console.error("Error fetching tariff data:", error);
        showErrorAlert();
      });

    const nameProject = document.getElementById("nameProjectText").value;
    const descriptionProject = document.getElementById(
      "descriptionProjectText"
    ).value;
    const descriptionFunnels = document.getElementById(
      "descriptionFunnelsText"
    ).value;
    const nameMetrics = document.getElementById("nameMetricsText").value;
    const descriptionMetrics = document.getElementById(
      "descriptionMetricsText"
    ).value;
    const targetValueMetric = document.getElementById(
      "targetValueMetricText"
    ).value;
    const additionalData = document.getElementById("additionalDataText").value;
    const imageProductDescription = document.getElementById(
      "imageProductDescriptionText"
    ).value;
    const selectedTariff = document.querySelector(
      'input[name="tariff"]:checked'
    )
      ? document.querySelector('input[name="tariff"]:checked').value
      : null;

    const photoInput = window.selectedFiles;

    // Сравнение для баланса
    if (selectedTariff === "standart-value" && defaultTariff < 0) {
      showErrorAlertNotMoney();
      return;
    }
    if (selectedTariff === "premium-value" && premiumTariff < 0) {
      showErrorAlertNotMoney();
      return;
    }

    if (
      nameProject.length === 0 ||
      descriptionProject.length === 0 ||
      descriptionFunnels.length === 0 ||
      nameMetrics.length === 0 ||
      descriptionMetrics.length === 0 ||
      targetValueMetric.length === 0 ||
      !selectedTariff ||
      photoInput.length === 0 ||
      imageProductDescription.length === 0
    ) {
      alert("Введите все данные!");
      return;
    }

    const formData = new FormData();
    for (let i = 0; i < photoInput.length; i++) {
      formData.append(`img_${i}`, photoInput[i], photoInput[i].name);
    }
    formData.append("img_description", imageProductDescription);
    formData.append("nameProject", nameProject);
    formData.append("descriptionProject", descriptionProject);
    formData.append("nameMetrics", nameMetrics);
    formData.append("descriptionMetrics", descriptionMetrics);
    formData.append("targetValueMetric", targetValueMetric);
    formData.append("additionalData", additionalData);
    formData.append("selectedTariff", selectedTariff);
    formData.append("descriptionFunnels", descriptionFunnels);

    loading.style.display = "block";
    card.style.display = "none";

    fetch("/new_project", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then(() => {
        loading.style.display = "none";
        showSuccessAlert();
      })
      .catch((error) => {
        loading.style.display = "none";
        card.style.display = "flex";
        showErrorAlert();
      });
  });
});

function showErrorAlertNotMoney() {
  const errorModalNotMoney = document.getElementById("errorModalNotMoney");
  const successBtn = document.getElementById("errorBtnNoMoney");

  errorModalNotMoney.style.display = "flex";

  successBtn.addEventListener("click", () => {
    errorModalNotMoney.style.display = "none";
  });
}

function showSuccessAlert() {
  const successModal = document.getElementById("successModal");
  const successBtn = document.getElementById("successBtn");

  successModal.style.display = "flex";

  successBtn.addEventListener("click", () => {
    successModal.style.display = "none";

    window.location.href = "/my_projects";
  });
}

function showErrorAlert() {
  const errorModal = document.getElementById("errorModal");
  const errorBtn = document.getElementById("errorBtn");

  errorModal.style.display = "flex";

  errorBtn.addEventListener("click", () => {
    errorModal.style.display = "none";
  });
}
