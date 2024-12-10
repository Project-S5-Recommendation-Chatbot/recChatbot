document.addEventListener('DOMContentLoaded', () => {
    const user = sessionStorage.getItem('user');
    const loginLink = document.getElementById('loginLink');
    if (user && loginLink) {
        loginLink.textContent = user;
        loginLink.href = '#'; // Prevent navigation back to the login page.
    }
});
