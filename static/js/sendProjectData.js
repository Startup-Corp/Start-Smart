
const btnSaveData = document.getElementById("generator-btn");
btnSaveData.addEventListener("click", () => {
    const nameProject = document.getElementById("nameProjectText").value;
    const descriptionProject = document.getElementById("descriptionProjectText").value;
    const descriptionFunnels = document.getElementById("descriptionFunnelsText").value;
    const nameMetrics = document.getElementById("nameMetricsText").value;
    const descriptionMetrics = document.getElementById("descriptionMetricsText").value;
    const targetValueMetric = document.getElementById("targetValueMetricText").value;
    const additionalData = document.getElementById("additionalDataText").value;

    const photoInput = document.getElementById('fileInput').files;;
    const imageProductDescription = document.getElementById('imageProductDescriptionText').value;

    const selectedTariff = document.querySelector('input[name="tariff"]:checked').value;

    if (nameProject.length == 0 ||
        descriptionProject.length == 0 ||
        descriptionFunnels.length == 0 ||
        nameMetrics.length == 0 ||
        descriptionMetrics.length == 0 ||
        targetValueMetric.length == 0 ||
        !selectedTariff ||
        photoInput.length == 0 ||
        imageProductDescription == 0) {
        alert("Введите все данные!");
        return;
    }

    const formData = new FormData();
    for (let i = 0; i < photoInput.length; i++) {
        formData.append('files[]', photoInput[i]);
    }
    formData.append('description', imageProductDescription);
    
    const data = {
        nameProject: nameProject,
        descriptionProject: descriptionProject,
        descriptionFunnels: descriptionFunnels,
        nameMetrics: nameMetrics,
        descriptionMetrics: descriptionMetrics,
        targetValueMetric: targetValueMetric,
        additionalData: additionalData,
        selectedTariff: selectedTariff,
        formData: formData,
    }

    fetch("/sendProjectData", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(() => {
            alert('Files successfully uploaded');
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error uploading files');
        });
});
