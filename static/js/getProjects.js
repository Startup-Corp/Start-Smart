

let logoProject = document.getElementsByClassName('rectangle');
let nameProject = document.getElementsByClassName('nameProject');
let disctProject = document.getElementsByClassName('descriptionProject');



async function getProjectsForUser() {
    const userData = {
        name: "Test User",
    };

    try {
        const projectsResponse = await fetch('/projects_page', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });

        if (!projectsResponse.ok) {
            throw new Error('Error fetching projects');
        }

        else {
            alert('Данные успешно получены!');
        }
      
        const projectsData = await projectsResponse.json();
        
        console.log('Projects:', projectsData);


    } catch (error) {
        console.error('Error:', error);
        alert('Error occurred while fetching projects.');
    }
}

// Вызываем функцию для получения проектов при загрузке страницы или в другом нужном месте
getProjectsForUser();