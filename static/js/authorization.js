const btnReg = document.getElementById("btn-authorization");

btnReg.addEventListener("click", async () => {
  const email = document.getElementById("mail").value;
  const password = document.getElementById("password").value;

  if (email.length === 0 || password.length === 0) {
    alert("Заполните все поля!");
    return;
  }
  const data = {
    email: email,
    passwordUser: password,
  };

  try {
    const response = await fetch("/auth", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      showSuccessAlert();
    } else if (response.status === 404) {
      showErrorAlert();
    }
  } catch (error) {
    alert(`Request failed: ${error.message}`);
  }
});

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