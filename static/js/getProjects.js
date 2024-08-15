// status - 0 = active
// status - 1 = disabled

async function getProjectsForUser() {
  const idData = {
    id: "8",
  };

  console.log(idData);

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
  // const tilesContainer = document.querySelector(".tiles");

  // projectsData.forEach((project) => {
  //   const article = document.createElement("article");
  //   article.classList.add("tile");

  //   const tileHeader = document.createElement("div");
  //   tileHeader.classList.add("tile-header");

  //   const h3 = document.createElement("h3");
  //   const span = document.createElement("span");
  //   span.textContent = project.name; // Используем название проекта из данных
  //   h3.appendChild(span);
  //   tileHeader.appendChild(h3);

  //   const currentStatusProject = document.createElement("div");
  //   currentStatusProject.classList.add("current-status-project");

  //   const statusProjectImg = document.createElement("img");
  //   statusProjectImg.src =
  //     project.status == "0"
  //       ? "static/css/Fonts/Project_status_icons/status-Active.svg"
  //       : "static/css/Fonts/Project_status_icons/status-Disabled.svg";
  //   statusProjectImg.classList.add("statusProject");
  //   statusProjectImg.alt = "альтернативный текст";
  //   currentStatusProject.appendChild(statusProjectImg);

  //   const link = document.createElement("a");
  //   link.href = "#";

  //   const linkSpan = document.createElement("span");
  //   linkSpan.textContent = "Перейти в проект";
  //   link.appendChild(linkSpan);

  //   const iconButton = document.createElement("span");
  //   iconButton.classList.add("icon-button");

  //   const iconImg = document.createElement("img");
  //   iconImg.src =
  //     "static/css/Fonts/Project_status_icons/right-arrow_87425.png";
  //   iconImg.alt = "альтернативный текст";
  //   iconButton.appendChild(iconImg);
  //   link.appendChild(iconButton);

  //   article.appendChild(tileHeader);
  //   article.appendChild(currentStatusProject);
  //   article.appendChild(link);

  //   // Добавляем элемент article в контейнер tiles
  //   tilesContainer.appendChild(article);
  // });
}

window.onload = async function () {
  await getProjectsForUser();
};
