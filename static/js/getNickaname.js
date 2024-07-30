async function getNickaname(idData) {
  console.log(idData);

  fetch("/set_nickname", {
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
  await getNickaname();
};
