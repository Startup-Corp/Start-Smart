const fileInput = document.getElementById('fileInput');
const fileDisplay = document.querySelector('.file-input-div ul');

fileInput.addEventListener('change', (event) => {
  const files = event.target.files;

//   // Очищаем список файлов
//   fileDisplay.innerHTML = ''; // Стираем все предыдущие элементы списка

  // Добавляем новые элементы в список
  for (const file of files) {
    const listItem = document.createElement('li');
    listItem.textContent = file.name;
    fileDisplay.appendChild(listItem);
  }
});
