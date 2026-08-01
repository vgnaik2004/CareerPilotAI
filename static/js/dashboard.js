// ===============================
// CareerPilot AI Dashboard
// ===============================

// Wait until page loads
document.addEventListener("DOMContentLoaded", function () {

    // ==========================
    // Fade In Animation
    // ==========================

    const cards = document.querySelectorAll(".card");

    cards.forEach((card, index) => {

        card.style.opacity = "0";
        card.style.transform = "translateY(40px)";

        setTimeout(() => {

            card.style.transition = "0.6s ease";
            card.style.opacity = "1";
            card.style.transform = "translateY(0px)";

        }, index * 150);

    });

    // ==========================
    // Progress Bar Animation
    // ==========================

    const progressBars = document.querySelectorAll(".progress-fill");

    progressBars.forEach(bar => {

        const width = bar.style.width;

        bar.style.width = "0%";

        setTimeout(() => {

            bar.style.transition = "width 2s ease";
            bar.style.width = width;

        }, 500);

    });

});

// ===============================
// Dark Mode
// ===============================

const darkBtn = document.getElementById("darkModeBtn");

darkBtn.addEventListener("click", () => {

    document.body.classList.toggle("dark-mode");

    if (document.body.classList.contains("dark-mode")) {

        darkBtn.innerHTML = "☀";

    }

    else {

        darkBtn.innerHTML = "🌙";

    }

});

// ===============================
// Card Hover Effect
// ===============================

const allCards = document.querySelectorAll(".card");

allCards.forEach(card => {

    card.addEventListener("mouseenter", () => {

        card.style.transform = "translateY(-8px) scale(1.02)";

    });

    card.addEventListener("mouseleave", () => {

        card.style.transform = "translateY(0px) scale(1)";

    });

});

// ===============================
// Notification Popup
// ===============================

window.onload = function () {

    setTimeout(() => {

        alert("🎉 Welcome to CareerPilot AI Dashboard!");

    }, 800);

};

// ===============================
// Resume Preview Scroll
// ===============================

const resume = document.querySelector("pre");

if (resume) {

    resume.style.scrollBehavior = "smooth";

}

// ===============================
// Console Message
// ===============================

console.log("CareerPilot AI Dashboard Loaded Successfully.");