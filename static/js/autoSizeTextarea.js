document.addEventListener("DOMContentLoaded", function () {
  const textareas = document.querySelectorAll("textarea");
  textareas.forEach(autoResizeTextarea);
});

function autoResizeTextarea(textarea) {
  textarea.style.height = "auto";
  textarea.style.height = textarea.scrollHeight + "px";
}

window.addEventListener("resize", function () {
  const textareas = document.querySelectorAll("textarea");
  textareas.forEach(autoResizeTextarea);
});