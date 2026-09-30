import json
import random


def load_questions():
    with open("data/questions.json", "r", encoding="utf-8") as file:
        return json.load(file)


def get_questions(role, experience, category, number=5):
    questions = load_questions()

    filtered_questions = []

    for question in questions:
        if (
            question["role"] == role
            and question["experience"] == experience
            and question["category"] == category
        ):
            filtered_questions.append(question)

    random.shuffle(filtered_questions)

    return filtered_questions[:number]