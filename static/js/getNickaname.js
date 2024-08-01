async function getNickaname(idData) {
  console.log(idData);

  fetch("/user_info", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    }
  })
    .then((response) => response.json())
    .then((data) => {
      const username = data['data']['user_data']['username'];
      let user_profile_block = document.getElementsByClassName('user-profile')[0];
      let username_span = user_profile_block.querySelectorAll('span')[0];
      username_span.textContent = username;
      console.log("Success:", data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

window.onload = async function () {
  await getNickaname();
};
