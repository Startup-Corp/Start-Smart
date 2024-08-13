document.addEventListener("DOMContentLoaded", () => {
  const btnSaveData = document.getElementById("generator-btn");

  btnSaveData.addEventListener("click", () => {
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

    fetch("/new_project", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then(() => {
        showSuccessAlert();
      })
      .catch((error) => {
        showErrorAlert();
      });
    });
  });
  
  function showErrorAlert() {
    Swal.fire({
      icon: "error",
      title: "Что-то пощло не так(",
      text: "Обратитесь в поддержку ТГ @AtikinNT",
      confirmButtonText: "OK",
      customClass: {
        confirmButton: "my-error-button",
      },
    });
}

function showSuccessAlert() {
  Swal.fire({
    icon: "success",
    title: "Успех",
    text: "Проект успешно создан",
    confirmButtonText: "Вернуться в Мои проекты",
    customClass: {
      confirmButton: "my-confirm-button",
    },
  }).then(() => {
    window.location.href = `${window.location.origin}/my_projects`;
  });
}