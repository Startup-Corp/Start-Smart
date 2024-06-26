document.getElementById('info-btn').addEventListener('click', function() {
    document.getElementById('info-form').classList.remove('hidden');
    document.getElementById('info-form').classList.add('visible');
    document.getElementById('security-form').classList.remove('visible');
    document.getElementById('security-form').classList.add('hidden');

    document.getElementById('info-btn').classList.add('active');
    document.getElementById('security-btn').classList.remove('active');
});

document.getElementById('security-btn').addEventListener('click', function() {
    document.getElementById('security-form').classList.remove('hidden');
    document.getElementById('security-form').classList.add('visible');
    document.getElementById('info-form').classList.remove('visible');
    document.getElementById('info-form').classList.add('hidden');

    document.getElementById('security-btn').classList.add('active');
    document.getElementById('info-btn').classList.remove('active');
});