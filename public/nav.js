document.addEventListener('DOMContentLoaded', () => {
    const user = JSON.parse(localStorage.getItem('user'));

    // Select nav elements
    const navDashboard = document.getElementById('nav-dashboard');
    const navAdmin = document.getElementById('nav-admin');
    const navCart = document.getElementById('nav-cart');
    const navAuth = document.getElementById('nav-auth');

    if (user) {
        // User is logged in
        if (navAuth) {
            navAuth.textContent = 'Logout';
            navAuth.href = '#';
            navAuth.addEventListener('click', (e) => {
                e.preventDefault();
                localStorage.removeItem('user');
                window.location.href = 'index.html';
            });
        }

        if (user.role === 'admin') {
            if (navAdmin) navAdmin.style.display = 'inline-block';
        } else {
            if (navDashboard) navDashboard.style.display = 'inline-block';
            if (navCart) navCart.style.display = 'inline-block';
        }
    }
});
