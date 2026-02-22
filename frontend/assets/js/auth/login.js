// frontend/assets/js/auth/login.js

document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");
    const phoneInput = document.getElementById("phone");
    const passwordInput = document.getElementById("password");
    const errorBox = document.getElementById("errorMessage");

    loginForm.addEventListener("submit", async function (e) {
        e.preventDefault();

        const payload = {
            phone: phoneInput.value.trim(),
            password: passwordInput.value.trim(),
        };

        // Basic validation
        if (!payload.phone || !payload.password) {
            showError("Please fill all fields.");
            return;
        }

        try {
            const data = await AuthAPI.login(payload);

            // Save token
            localStorage.setItem("access_token", data.access_token);
            localStorage.setItem("user_role", data.role);
            localStorage.setItem("user_id", data.user_id);
            localStorage.setItem("user_name", data.name);

            // Redirect based on role
            if (data.role === "farmer") {
                window.location.href = "../dashboards/farmer/farmer-dashboard.html";
            } else if (data.role === "buyer") {
                window.location.href = "../dashboards/buyer/buyer-dashboard.html";
            } else if (data.role === "admin") {
                window.location.href = "../dashboards/admin/admin-dashboard.html";
            } else {
                showError("Unknown user role.");
            }

        } catch (error) {
            showError(error.message || "Login failed.");
        }
    });

    function showError(message) {
        if (errorBox) {
            errorBox.innerText = message;
            errorBox.style.display = "block";
        } else {
            alert(message);
        }
    }
});