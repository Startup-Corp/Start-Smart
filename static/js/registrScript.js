const btnReg = document.getElementById("btn-registr");

btnReg.addEventListener("click", async () => {
  const name = document.getElementById("name").value;
  const mail = document.getElementById("mail").value;
  const password = document.getElementById("password").value;
  const repPassword = document.getElementById("repPassword").value;

  if (password.length < 6 || repPassword.length < 6){
    alert("Пароль должен превышать 5 символов");
    return;
  }

  if (password !== repPassword) {
    alert("Пароли не совпадают!");
    return;
  } else if (
    name.length === 0 ||
    name.length === 0 ||
    password.length === 0 ||
    repPassword.length === 0
  ) {
    alert("Введите все поля!");
    return;
  }
  
  const data = {
    name: name,
    email: mail,
    password: password,
  };

  const response = await fetch("/new_user", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (response.ok) {
    showSuccessAlert();
  } else {
    showErrorAlert();
  }
});

function showSuccessAlert() {
  Swal.fire({
    icon: "success",
    title: "Успех",
    text: "Добро пожаловать!",
    customClass: {
      confirmButton: "my-confirm-button",
    },
  }).then(() => {
    window.location.href = `/my_projects`;
  });
}

function showErrorAlert() {
  Swal.fire({
    icon: "error",
    title: "Ошибка",
    text: "Не удалось отправить данные!",
    confirmButtonText: "Попробовать снова",
    customClass: {
      confirmButton: "my-error-button",
    },
  });
}
