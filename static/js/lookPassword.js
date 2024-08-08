const togglePassword = document.getElementById("toggle-password");
if (togglePassword) {
  togglePassword.addEventListener("click", function () {
    let passwordInput = document.getElementById("password");
    let eyeIcon = document.getElementById("eye-icon");

    if (passwordInput.type === "password") {
      passwordInput.type = "text";
      eyeIcon.src =
        "/static/css/Fonts/Icons_for_registration/icons8-eye-slash.svg"; // скрыть пароль
    } else {
      passwordInput.type = "password";
      eyeIcon.src = "/static/css/Fonts/Icons_for_registration/icons8-eye.svg"; // показать пароли
    }
  });
}
const toggleRepPassword = document.getElementById("toggle-repPassword");
if (toggleRepPassword) {
  toggleRepPassword.addEventListener("click", function () {
    let passwordRepInput = document.getElementById("repPassword");
    let eyeIcon = document.getElementById("eye-icon-rep");

    if (passwordRepInput.type === "password") {
      passwordRepInput.type = "text";
      eyeIcon.src =
        "/static/css/Fonts/Icons_for_registration/icons8-eye-slash.svg"; // скрыть пароль
    } else {
      passwordRepInput.type = "password";
      eyeIcon.src = "/static/css/Fonts/Icons_for_registration/icons8-eye.svg"; // показать пароли
    }
  });
}

