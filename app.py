from flask import Flask, render_template, request, redirect, url_for
from storage import initialize_database, save_quiz, get_quizzes, get_quiz, save_question, get_questions, delete_question

app = Flask(__name__)
initialize_database()

@app.route("/")
def welcome():
    quizzes = get_quizzes()
    return render_template("index.html", quizzes=quizzes)

@app.route("/create", methods=["GET", "POST"])
def create_quiz():
    if request.method == "POST":
        print("Form submitted!")
        quiz_name = request.form.get("quiz_name")
        print("Quiz Name:", quiz_name)
        save_quiz(quiz_name)
    return render_template("create_quiz.html")

@app.route("/quiz/<int:quiz_id>")
def view_quiz(quiz_id):
    quiz = get_quiz(quiz_id)
    questions = get_questions(quiz_id)
    print("Questions:", questions)
    print("Quiz: ", quiz)
    return render_template("view_quiz.html", quiz=quiz, questions=questions)

@app.route("/quiz/<int:quiz_id>/add-question", methods=["GET", "POST"])
def add_question(quiz_id):
    if request.method == "POST":
        question = request.form.get("question")
        answer_a = request.form.get("answer_a")
        answer_b = request.form.get("answer_b")
        answer_c = request.form.get("answer_c")
        answer_d = request.form.get("answer_d")
        correct_answer = request.form.get("correct_answer")
        save_question(quiz_id, question, answer_a, answer_b, answer_c, answer_d, correct_answer)
        return redirect(url_for("view_quiz", quiz_id=quiz_id))
    return render_template("add_question.html", quiz_id=quiz_id)

@app.route("/quiz/<int:quiz_id>/take-quiz", methods=["GET", "POST"])
def take_quiz(quiz_id):
    quiz = get_quiz(quiz_id)
    questions = get_questions(quiz_id)
    if request.method == "POST":
        score = 0
        results = []
        for question in questions:
            user_answer = request.form.get(f"question_{question[0]}")
            is_correct = user_answer == question[7]
            if is_correct:
                score += 1
            results.append({
                "question": question[2],
                "user_answer": user_answer,
                "correct_answer": question[7],
                "is_correct": is_correct

            })
        return render_template("results.html", quiz=quiz, score=score, total=len(questions), results=results)
    return render_template("take_quiz.html", quiz=quiz, questions=questions)

@app.route("/quiz/<int:quiz_id>/question/<int:question_id>/delete", methods=["POST"])
def delete_question_route(quiz_id, question_id):
    delete_question(question_id)
    return redirect(url_for("view_quiz", quiz_id=quiz_id))

if __name__ == "__main__":
    app.run(debug=True)