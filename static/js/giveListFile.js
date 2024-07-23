const fileInput = document.getElementById("fileInput");
const fileDisplay = document.querySelector(".file-input-div ul");
const maxCountFile = 5;

fileInput.addEventListener("change", (event) => {
  const files = event.target.files;

  if (files.length > maxCountFile) {
    alert(`Можно выбрать не более ${maxCountFile} файлов.`);
    fileInput.value = "";
    return;
  }

  for (const file of files) {
    const listItem = document.createElement("li");
    listItem.textContent = file.name;
    fileDisplay.appendChild(listItem);
  }
});
