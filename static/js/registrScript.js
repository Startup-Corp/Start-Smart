const btnReg = document.getElementById('btn-registr');

btnReg.addEventListener('click', async ()=> {
    const name = document.getElementById('name').value;
    const mail = document.getElementById('mail').value;
    const password = document.getElementById('password').value;
    const repPassword = document.getElementById('repPassword').value; 

    if (password !== repPassword) {
        alert('Пароли не совпадают');
    } else {
        const data = {
            nameUser: name,
            mailUser: mail,
            passwordUser: password,
        };
        
        const response = await fetch('/add_user', {
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
    }


});