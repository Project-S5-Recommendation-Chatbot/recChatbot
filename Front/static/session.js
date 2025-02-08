// document.addEventListener('DOMContentLoaded', () => {
//     const user = sessionStorage.getItem('user');
//     const loginLink = document.getElementById('loginLink');
//     if (user && loginLink) {
//         loginLink.textContent = user;
//         loginLink.href = '#'; // Prevent navigation back to the login page.
//     }
// });
document.addEventListener('DOMContentLoaded', function() {
    const loginLink = document.getElementById('loginLink');
    const user = sessionStorage.getItem('user');

    if (loginLink) {
        if (user) {
            loginLink.textContent = user + " - Logout";
            loginLink.href = 'javascript:void(0);'; // Prevent default link behavior
            loginLink.onclick = logout; // Assign logout function
        } else {
            loginLink.textContent = 'Login';
            loginLink.href = 'login.html';
            loginLink.onclick = null; // Ensure no logout function is attached
        }
    }

    function logout() {
        sessionStorage.removeItem('user');
        alert('Logged out successfully!');
        window.location.href = 'https://raw.githubusercontent.com/Project-S5-Recommendation-Chatbot/recChatbot/frontend/Front/templates/index.html'; // Redirect to home page after logout
    }
});
