const buttonSubmut = document.getElementById("zapisatsya");

buttonSubmut.addEventListener('click', async () => {
    const nameText = document.getElementById("name").value;
    const phoneNumber = document.getElementById('phoneNumber').value;
    const nameProject = document.getElementById('nameProject').value;

    // console.log(nameText);
    // console.log(phoneNumber);
    // console.log(nameProject);

    const data = {
        name: nameText,
        phone: phoneNumber,
        project: nameProject,
    }

    //Отправка данных на сервер
    const response = await fetch('/save_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        alert('Data saved successfully!');
    } else {
        alert('Error occurred while saving data.');
    }
});