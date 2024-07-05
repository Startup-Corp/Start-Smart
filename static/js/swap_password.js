const btnSave = document.getElementById("save-btn");
btnSave.addEventListener("click", () => {
  const oldPassword = document.getElementById("old-password").value;
  const newPassword = document.getElementById("new-password").value;
  const repPassword = document.getElementById("repeat-password").value;

  if (
    oldPassword.length == 0 ||
    newPassword.length == 0 ||
    repPassword.length == 0
  ) {
    alert("Введите данные!");
  }

  if (newPassword !== repPassword) {
    alert("Пароли не совпадают!");
  } else {
    alert("Пароль типа поменялся");
  }
});

const btnClose = document.getElementById("close-btn");
btnClose.addEventListener("click", () => {
  document.getElementById("old-password").value = "";
  document.getElementById("new-password").value = "";
  document.getElementById("repeat-password").value = "";
});
