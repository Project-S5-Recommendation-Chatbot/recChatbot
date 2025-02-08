// document.addEventListener('DOMContentLoaded', () => {
//     const user = sessionStorage.getItem('user');
//     const loginLink = document.getElementById('loginLink');
//     if (user && loginLink) {
//         loginLink.textContent = user;
//         loginLink.href = '#'; // Prevent navigation back to the login page.
//     }
// });
document.addEventListener("DOMContentLoaded", function () {
    const user = sessionStorage.getItem("user");
    const loginLink = document.getElementById("loginLink");

    if (user) {
        loginLink.textContent = user;
        loginLink.removeAttribute("href");
        loginLink.style.cursor = "default";
        loginLink.style.opacity = "0.6"; // Make it look disabled
    }
});
