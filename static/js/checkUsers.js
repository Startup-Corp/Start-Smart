const btnReg = document.getElementById("btn-authorization");

btnReg.addEventListener("click", async () => {
  const mail = document.getElementById("mail").value;
  const password = document.getElementById("password").value;

  const data = {
    mailUser: mail,
    passwordUser: password,
  };

  try {
    const response = await fetch("/get_user", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      alert("Добро пожаловать!");

      window.location.href = "http://127.0.0.1:5000/my_projects";
    } else if (response.status === 404) {
      alert("Пользователь не найден");
    }
  } catch (error) {
    alert(`Request failed: ${error.message}`);
  }
});
