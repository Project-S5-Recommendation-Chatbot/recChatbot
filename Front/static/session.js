// document.addEventListener('DOMContentLoaded', () => {
//     const user = sessionStorage.getItem('user');
//     const loginLink = document.getElementById('loginLink');
//     if (user && loginLink) {
//         loginLink.textContent = user;
//         loginLink.href = '#'; // Prevent navigation back to the login page.
//     }
// });

document.addEventListener('DOMContentLoaded', () => {
    const user = sessionStorage.getItem('user');
    const loginLink = document.getElementById('loginLink');

    if (user && loginLink) {
        loginLink.textContent = `${user} (Logout)`;
        loginLink.href = '#'; // Prevent navigation back to the login page.

        // Add logout functionality
        loginLink.addEventListener('click', (event) => {
            event.preventDefault();
            sessionStorage.removeItem('user');
            window.location.reload(); // Refresh the page to reflect logout
        });
    }
});
