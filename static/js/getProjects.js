let logoProject = document.getElementsByClassName("rectangle");
let nameProject = document.getElementsByClassName("nameProject");
let disctProject = document.getElementsByClassName("descriptionProject");

async function getProjectsForUser() {
  const idData = {
    data: '8',
  };

  try {
    const projectsResponse = await fetch("/get_projects", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(idData),
      
    });
    
    console.log(body);
    // if (!projectsResponse.ok) {
    //   throw new Error("Error fetching projects");
    // } else {
    //   alert("Данные успешно получены!");
    // }

    // const projectsData = await projectsResponse.json();

    // // Получаем контейнер, в который будем вставлять данные о проектах
    // const projectsContainer = document.getElementById("projectsContainer");

    // // // Очищаем контейнер перед добавлением новых данных (если это нужно)
    // // projectsContainer.innerHTML = '';

    // // Проходимся по каждому проекту и создаем соответствующий HTML-элемент
    // projectsData.forEach((project) => {
    //   const projectElement = document.createElement("div");
    //   projectElement.classList.add("projectsOne");

    //   const rectangle = document.createElement("div");
    //   rectangle.classList.add("rectangle");

    //   const nameProject = document.createElement("p");
    //   nameProject.classList.add("nameProject");
    //   nameProject.textContent = project.name;

    //   const descriptionProject = document.createElement("div");
    //   descriptionProject.classList.add("descriptionProject");
    //   descriptionProject.textContent = project.description;

    //   projectElement.appendChild(rectangle);
    //   projectElement.appendChild(nameProject);
    //   projectElement.appendChild(descriptionProject);

    //   // Добавляем созданный элемент в контейнер
    //   projectsContainer.appendChild(projectElement);
    // });

    console.log("Projects:", projectsData);
  } catch (error) {
    console.error("Error:", error);
    alert("Error occurred while fetching projects.");
  }
}

// window.onload = async function () {
//   await getProjectsForUser();
// };
