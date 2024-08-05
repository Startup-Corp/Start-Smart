// status - 0 = active
// status - 1 = disabled

async function getProjectsForUser() {

  fetch("/projects", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(idData),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Success:", data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

window.onload = async function () {
  await getProjectsForUser();
};
