// Optional: Add JavaScript to control the gallery rotation speed or direction
document.addEventListener('DOMContentLoaded', function() {
    const gallery = document.querySelector('.gallery');
    let isPaused = false;

    gallery.addEventListener('mouseover', function() {
        gallery.style.animationPlayState = 'paused';
        isPaused = true;
    });

    gallery.addEventListener('mouseout', function() {
        gallery.style.animationPlayState = 'running';
        isPaused = false;
    });
});

//for login and logout handle
document.addEventListener('DOMContentLoaded', function() {
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');

    // Check if the user is logged in (e.g., check for a token in local storage)
    const isLoggedIn = localStorage.getItem('authToken') !== null;

    if (isLoggedIn) {
        loginLink.style.display = 'none';
        logoutLink.style.display = 'block';
    } else {
        loginLink.style.display = 'block';
        logoutLink.style.display = 'none';
    }

    // Handle logout
    logoutLink.addEventListener('click', function(event) {
        event.preventDefault();
        // Remove the token from local storage
        localStorage.removeItem('authToken');
        // Redirect to the login page
        window.location.href = '/login';
    });
});