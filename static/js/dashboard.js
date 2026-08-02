// ==========================================
// CareerPilot AI Dashboard
// ==========================================

document.addEventListener("DOMContentLoaded", function () {

    // ===============================
    // Dark Mode
    // ===============================

    const darkBtn = document.getElementById("darkModeBtn");

    if (darkBtn) {

        if (localStorage.getItem("theme") === "dark") {
            document.body.classList.add("dark");
            darkBtn.innerHTML = "☀️";
        }

        darkBtn.addEventListener("click", function () {

            document.body.classList.toggle("dark");

            if (document.body.classList.contains("dark")) {

                localStorage.setItem("theme", "dark");
                darkBtn.innerHTML = "☀️";

            } else {

                localStorage.setItem("theme", "light");
                darkBtn.innerHTML = "🌙";

            }

        });

    }

    // ===============================
    // Animated Counters
    // ===============================

    const numbers = document.querySelectorAll(".stat-card h2");

    numbers.forEach(counter => {

        let text = counter.innerText.replace("%", "");
        let target = parseInt(text);

        if (isNaN(target)) return;

        let count = 0;

        let speed = Math.max(10, target / 60);

        const update = () => {

            if (count < target) {

                count += speed;

                if (count > target)
                    count = target;

                if (counter.innerText.includes("%")) {
                    counter.innerHTML = Math.floor(count) + "%";
                } else {
                    counter.innerHTML = Math.floor(count);
                }

                requestAnimationFrame(update);

            }

        };

        update();

    });

    // ===============================
    // ATS Chart
    // ===============================

    const atsCanvas = document.getElementById("atsChart");

    if (atsCanvas) {

        const atsScore =
            parseInt(document.querySelectorAll(".stat-card h2")[0].innerText);

        const jobMatch =
            parseInt(document.querySelectorAll(".stat-card h2")[1].innerText);

        new Chart(atsCanvas, {

            type: "bar",

            data: {

                labels: ["ATS Score", "Job Match"],

                datasets: [{

                    data: [atsScore, jobMatch],

                    backgroundColor: [
                        "#2563eb",
                        "#22c55e"
                    ],

                    borderRadius: 10

                }]

            },

            options: {

                responsive: true,

                plugins: {

                    legend: {

                        display: false

                    }

                },

                scales: {

                    y: {

                        beginAtZero: true,

                        max: 100

                    }

                }

            }

        });

    }

    // ===============================
    // Skills Chart
    // ===============================

    const skillsCanvas = document.getElementById("skillsChart");

    if (skillsCanvas) {

        const skills =
            document.querySelectorAll(".stat-card h2")[2].innerText;

        const missing =
            document.querySelectorAll(".stat-card h2")[3].innerText;

        new Chart(skillsCanvas, {

            type: "doughnut",

            data: {

                labels: [
                    "Skills Found",
                    "Missing Skills"
                ],

                datasets: [{

                    data: [
                        parseInt(skills),
                        parseInt(missing)
                    ],

                    backgroundColor: [
                        "#22c55e",
                        "#ef4444"
                    ]

                }]

            },

            options: {

                responsive: true,

                plugins: {

                    legend: {

                        position: "bottom"

                    }

                }

            }

        });

    }

    // ===============================
    // Card Hover Animation
    // ===============================

    const cards = document.querySelectorAll(".stat-card, .panel");

    cards.forEach(card => {

        card.addEventListener("mouseenter", function () {

            this.style.transform = "translateY(-8px)";

        });

        card.addEventListener("mouseleave", function () {

            this.style.transform = "translateY(0px)";

        });

    });

    // ===============================
    // Notification Animation
    // ===============================

    const bell = document.querySelector(".notification");

    if (bell) {

        setInterval(() => {

            bell.classList.toggle("text-warning");

        }, 1000);

    }

});