// ===========================================
// CareerPilot AI - Register Page
// ===========================================

document.addEventListener("DOMContentLoaded", () => {

    // ===============================
    // Show / Hide Password
    // ===============================

    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("confirmPassword");
    const togglePassword = document.getElementById("togglePassword");

    if (togglePassword && password) {

        togglePassword.addEventListener("click", () => {

            const type =
                password.getAttribute("type") === "password"
                    ? "text"
                    : "password";

            password.setAttribute("type", type);

            togglePassword.innerHTML =
                type === "password"
                    ? '<i class="bi bi-eye-fill"></i>'
                    : '<i class="bi bi-eye-slash-fill"></i>';

        });

    }

    // ===============================
    // Password Strength
    // ===============================

    const strengthBar = document.getElementById("strengthBar");
    const message = document.getElementById("passwordMessage");

    if (password) {

        password.addEventListener("input", () => {

            let value = password.value;

            let strength = 0;

            if (value.length >= 8) strength++;
            if (/[A-Z]/.test(value)) strength++;
            if (/[a-z]/.test(value)) strength++;
            if (/[0-9]/.test(value)) strength++;
            if (/[^A-Za-z0-9]/.test(value)) strength++;

            switch (strength) {

                case 1:

                    strengthBar.style.width = "20%";
                    strengthBar.style.background = "#ef4444";
                    message.innerHTML = "Weak Password";
                    break;

                case 2:

                    strengthBar.style.width = "40%";
                    strengthBar.style.background = "#f97316";
                    message.innerHTML = "Fair Password";
                    break;

                case 3:

                    strengthBar.style.width = "60%";
                    strengthBar.style.background = "#eab308";
                    message.innerHTML = "Good Password";
                    break;

                case 4:

                    strengthBar.style.width = "80%";
                    strengthBar.style.background = "#22c55e";
                    message.innerHTML = "Strong Password";
                    break;

                case 5:

                    strengthBar.style.width = "100%";
                    strengthBar.style.background = "#16a34a";
                    message.innerHTML = "Very Strong Password";
                    break;

                default:

                    strengthBar.style.width = "0%";
                    message.innerHTML = "";

            }

        });

    }

    // ===============================
    // Confirm Password Validation
    // ===============================

    if (confirmPassword && password) {

        confirmPassword.addEventListener("keyup", () => {

            if (confirmPassword.value === "")
                return;

            if (password.value === confirmPassword.value) {

                confirmPassword.style.border = "2px solid #22c55e";

            } else {

                confirmPassword.style.border = "2px solid #ef4444";

            }

        });

    }

    // ===============================
    // Mobile Validation
    // ===============================

    const mobile = document.querySelector('input[name="mobile"]');

    if (mobile) {

        mobile.addEventListener("input", () => {

            mobile.value = mobile.value.replace(/[^0-9]/g, "");

            if (mobile.value.length > 10) {

                mobile.value = mobile.value.slice(0, 10);

            }

        });

    }

    // ===============================
    // Graduation Year Validation
    // ===============================

    const year = document.querySelector('input[name="graduation_year"]');

    if (year) {

        year.addEventListener("input", () => {

            if (year.value < 2020)
                year.value = 2020;

            if (year.value > 2035)
                year.value = 2035;

        });

    }

    // ===============================
    // Register Button Loading
    // ===============================

    const form = document.querySelector(".register-form");
    const button = document.querySelector(".register-btn");

    if (form && button) {

        form.addEventListener("submit", () => {

            button.disabled = true;

            button.innerHTML =
                '<span class="spinner-border spinner-border-sm"></span> Creating Account...';

        });

    }

    // ===============================
    // Smooth Fade
    // ===============================

    document.body.style.opacity = "0";

    setTimeout(() => {

        document.body.style.transition = "opacity .5s";

        document.body.style.opacity = "1";

    }, 100);

});