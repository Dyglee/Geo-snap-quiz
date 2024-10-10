function showForm(formType) {
    const loginForm = document.getElementById('login-form-container');
    const signupForm = document.getElementById('signup-form-container');

    if (formType === 'login') {
        loginForm.style.display = 'block';
        signupForm.style.display = 'none';
    } else if (formType === 'signup') {
        signupForm.style.display = 'block';
        loginForm.style.display = 'none';
    }
}

function validateSignupForm() {
    const email = document.getElementById('signup-email').value;
    const confirmEmail = document.getElementById('confirm-email').value;
    const password = document.getElementById('signup-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    if (email !== confirmEmail) {
        alert('Emails do not match!');
        return false;
    }

    if (password !== confirmPassword) {
        alert('Passwords do not match!');
        return false;
    }

    return true;  // Allow form submission if validation passes
}