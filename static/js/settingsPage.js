document.addEventListener("DOMContentLoaded", async function() {
    const profileButton = document.getElementById("profileButton");
    const securityButton = document.getElementById("securityButton");

    profileButton.addEventListener("click", function() {
        profileButton.classList.add("active");
        securityButton.classList.remove("active");
        document.getElementById('windowProfile').style.display = 'flex';
        document.getElementById('windowSafetySection').style.display = 'none';
    });

    securityButton.addEventListener("click", function() {
        profileButton.classList.remove("active");
        securityButton.classList.add("active");
        document.getElementById('windowProfile').style.display = 'none';
        document.getElementById('windowSafetySection').style.display = 'flex';
    });
});

