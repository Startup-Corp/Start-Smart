document.getElementById('showModalBtn').addEventListener('click', function() {
    document.getElementById('overlay').style.display = 'block';
    document.getElementById('modal').style.display = 'grid';
});

document.querySelector('.close').addEventListener('click', function() {
    document.getElementById('overlay').style.display = 'none';
    document.getElementById('modal').style.display = 'none';
});