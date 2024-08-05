const fileInput = document.getElementById("fileInput");
const fileDisplay = document.querySelector(".file-input-div ul");
const maxCountFile = 3;
let currentFileCount = 0;

fileInput.addEventListener("change", (event) => {
  const files = event.target.files;
  const validExtensions = ["image/png", "image/jpeg"];

  if (currentFileCount + files.length > maxCountFile) {
    alert(`Можно выбрать не более ${maxCountFile} файлов.`);
    fileInput.value = "";
    return;
  }

  for (const file of files) {
    if (!validExtensions.includes(file.type)) {
      alert("Можно прикреплять только файлы с расширениями .png и .jpg.");
      fileInput.value = "";
      return;
    }
  }

  for (const file of files) {
    const listItem = document.createElement("li");
    listItem.textContent = file.name;

    listItem.addEventListener("click", () => {
      listItem.remove();
      currentFileCount--;
    });

    fileDisplay.appendChild(listItem);
  }

  currentFileCount += files.length;
  fileInput.value = "";
});
