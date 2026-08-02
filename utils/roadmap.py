def get_roadmap(role):

    roadmap = {

        "Frontend Developer": [
            "Learn HTML",
            "Learn CSS",
            "Learn JavaScript",
            "Learn Bootstrap",
            "Learn React.js",
            "Learn Git & GitHub",
            "Build 5 Frontend Projects",
            "Deploy Portfolio Website"
        ],

        "Backend Developer": [
            "Learn Python",
            "Learn Flask",
            "Learn Django",
            "Learn SQL",
            "Learn REST APIs",
            "Learn Authentication",
            "Build Backend Projects",
            "Deploy on Render"
        ],

        "Full Stack Developer": [
            "HTML, CSS, JavaScript",
            "React.js",
            "Python Flask",
            "MySQL",
            "REST API",
            "Git & GitHub",
            "Docker Basics",
            "Deploy Full Stack Project"
        ],

        "Python Developer": [
            "Python Basics",
            "OOP Concepts",
            "File Handling",
            "Flask",
            "Django",
            "MySQL",
            "REST API",
            "Build Python Projects"
        ],

        "AI Engineer": [
            "Python",
            "NumPy",
            "Pandas",
            "Matplotlib",
            "Machine Learning",
            "Deep Learning",
            "TensorFlow",
            "Build AI Projects"
        ]
    }

    return roadmap.get(
        role,
        [
            "Learn Programming Fundamentals",
            "Build Projects",
            "Practice Interview Questions",
            "Apply for Jobs"
        ]
    )