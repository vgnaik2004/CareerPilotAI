# ==========================================
# CareerPilot AI
# Skills Detection Engine - Part 1
# ==========================================

SKILLS = [

    # -------------------------
    # Programming Languages
    # -------------------------

    "Python",
    "Java",
    "C",
    "C++",
    "C#",
    "JavaScript",
    "TypeScript",
    "Go",
    "Rust",
    "PHP",
    "Ruby",
    "Kotlin",
    "Swift",
    "R",
    "MATLAB",

    # -------------------------
    # Frontend
    # -------------------------

    "HTML",
    "HTML5",
    "CSS",
    "CSS3",
    "Bootstrap",
    "Tailwind CSS",
    "React",
    "Angular",
    "Vue",
    "Next.js",
    "jQuery",

    # -------------------------
    # Backend
    # -------------------------

    "Node.js",
    "Express.js",
    "Flask",
    "Django",
    "FastAPI",
    "Spring Boot",
    "ASP.NET",
    "Laravel",

    # -------------------------
    # Databases
    # -------------------------

    "SQL",
    "MySQL",
    "PostgreSQL",
    "SQLite",
    "Oracle",
    "MongoDB",
    "Firebase",

    # -------------------------
    # Version Control
    # -------------------------

    "Git",
    "GitHub",
    "GitLab",

    # -------------------------
    # IDE & Tools
    # -------------------------

    "VS Code",
    "Visual Studio",
    "PyCharm",
    "Eclipse",
    "IntelliJ IDEA",
    "Android Studio",
    "MATLAB",
    "Postman",
    "Figma",
    "Canva",

    # -------------------------
    # CS Fundamentals
    # -------------------------

    "Data Structures",
    "Algorithms",
    "OOP",
    "DBMS",
    "Operating Systems",
    "Computer Networks",
    "REST API",
    "JSON",
    "XML"

]


def extract_skills(text):

    found_skills = []

    text_lower = text.lower()

    for skill in SKILLS:

        if skill.lower() in text_lower:
            found_skills.append(skill)

    return sorted(list(set(found_skills)))