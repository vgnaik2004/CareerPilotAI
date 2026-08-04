// ======================================
// CareerPilot AI - Profile JS
// ======================================

document.addEventListener("DOMContentLoaded", function () {

    // ============================
    // Dark Mode
    // ============================

    const themeToggle = document.getElementById("themeToggle");

    if (themeToggle) {

        // Load saved theme
        if (localStorage.getItem("theme") === "dark") {
            document.body.classList.add("dark");
            themeToggle.checked = true;
        }

        themeToggle.addEventListener("change", function () {

            if (this.checked) {

                document.body.classList.add("dark");
                localStorage.setItem("theme", "dark");

            } else {

                document.body.classList.remove("dark");
                localStorage.setItem("theme", "light");

            }

        });

    }

    // ============================
    // Card Hover Animation
    // ============================

    const cards = document.querySelectorAll(".card,.profile-box");

    cards.forEach(card => {

        card.addEventListener("mouseenter", function () {

            this.style.transform = "translateY(-5px)";

        });

        card.addEventListener("mouseleave", function () {

            this.style.transform = "translateY(0px)";

        });

    });

    // ============================
    // Edit Profile Button
    // ============================

    const editBtn = document.querySelector(".edit-btn");

    if (editBtn) {

        editBtn.addEventListener("click", function () {

            alert("Edit Profile feature will be added soon.");

        });

    }

    // ============================
    // Email Notification Toggle
    // ============================

    const switches = document.querySelectorAll(".switch input");

    switches.forEach(toggle => {

        toggle.addEventListener("change", function () {

            console.log("Preference Updated");

        });

    });

    // ============================
    // Smooth Page Fade
    // ============================

    document.body.style.opacity = "0";

    setTimeout(() => {

        document.body.style.transition = "opacity .4s";
        document.body.style.opacity = "1";

    }, 100);

});