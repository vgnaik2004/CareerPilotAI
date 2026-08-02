def get_interview_questions(role):

    questions = {

        "Frontend Developer": [

            "What is HTML?",

            "What is CSS?",

            "Difference between Flexbox and Grid?",

            "Explain JavaScript closures.",

            "What is React?"
        ],

        "Python Developer": [

            "What are Python decorators?",

            "Difference between List and Tuple?",

            "Explain OOP concepts.",

            "What is Flask?",

            "What is Django?"
        ],

        "AI Engineer": [

            "What is Machine Learning?",

            "Difference between AI and ML?",

            "What is Deep Learning?",

            "Explain Neural Networks.",

            "What is NLP?"
        ]
    }

    return questions.get(
        role,
        ["No interview questions available."]
    )