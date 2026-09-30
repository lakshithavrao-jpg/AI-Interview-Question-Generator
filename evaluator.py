import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return text


def evaluate_answer(user_answer, question_data):

    user_answer = clean_text(user_answer)
    ideal_answer = clean_text(question_data["ideal_answer"])

    keywords = question_data["keywords"]

    # Keyword matching
    matched_keywords = []

    for keyword in keywords:
        if keyword.lower() in user_answer:
            matched_keywords.append(keyword)

    missing_keywords = [
        keyword for keyword in keywords
        if keyword.lower() not in user_answer
    ]

    # Semantic similarity
    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([
        user_answer,
        ideal_answer
    ])

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    similarity_score = similarity * 10

    # Keyword score
    if len(keywords) > 0:
        keyword_score = (
            len(matched_keywords) / len(keywords)
        ) * 10
    else:
        keyword_score = 0

    # Final score
    final_score = (
        similarity_score * 0.6
        + keyword_score * 0.4
    )

    final_score = min(round(final_score, 1), 10)

    # Feedback
    if final_score >= 8:
        feedback = "Excellent answer. Your response covers most important concepts."

    elif final_score >= 6:
        feedback = "Good answer, but some important concepts could be explained more clearly."

    elif final_score >= 4:
        feedback = "Your answer has some relevant information, but several important concepts are missing."

    else:
        feedback = "Your answer needs improvement. Try explaining the main concepts more clearly."

    return {
        "score": final_score,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "feedback": feedback,
        "ideal_answer": question_data["ideal_answer"]
    }