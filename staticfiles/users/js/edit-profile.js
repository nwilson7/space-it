document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("edit-password-form");

    form.addEventListener("submit", function(event) {
        let isValid = true;

        // Clear previous error messages
        document.querySelectorAll(".error-message").forEach(el => el.textContent = "");

        // Password validation
        const password1 = document.getElementById("password1");
        const password2 = document.getElementById("password2");

        if (password1.value.length < 6) {
            document.getElementById("password1-error").textContent = "Password must be at least 6 characters.";
            isValid = false;
        }

        if (password1.value !== password2.value) {
            document.getElementById("password2-error").textContent = "Passwords do not match.";
            isValid = false;
        }

        // Prevent form submission if invalid
        if (!isValid) {
            event.preventDefault();
        }
    });
});
