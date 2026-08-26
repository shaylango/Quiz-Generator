from flask import Flask, render_template, request, redirect, url_for, abort
from storage import initialize_database, save_quiz, get_quizzes, get_quiz, save_question, get_questions, delete_question, get_question, update_question, update_quiz, delete_quiz

app = Flask(__name__)
initialize_database()

@app.route("/")
def welcome():
    quizzes = get_quizzes()
    return render_template("index.html", quizzes=quizzes)

@app.route("/create", methods=["GET", "POST"])
def create_quiz():
    if request.method == "POST":
        quiz_name = request.form.get("quiz_name", "")
        if not quiz_name.strip():
            return render_template("create_quiz.html", quiz_name=quiz_name, error="Quiz name is required")
        save_quiz(quiz_name)
        return redirect(url_for("welcome"))
    return render_template("create_quiz.html", quiz_name="")

@app.route("/quiz/<int:quiz_id>")
def view_quiz(quiz_id):
    quiz = get_quiz(quiz_id)
    if not quiz:
        abort(404)
    questions = get_questions(quiz_id)
    print("Questions:", questions)
    print("Quiz: ", quiz)
    return render_template("view_quiz.html", quiz=quiz, questions=questions)

@app.route("/quiz/<int:quiz_id>/add-question", methods=["GET", "POST"])
def add_question(quiz_id):
    quiz = get_quiz(quiz_id)
    if not quiz:
        abort(404)
    if request.method == "POST":
        question = request.form.get("question", "")
        answer_a = request.form.get("answer_a", "")
        answer_b = request.form.get("answer_b", "")
        answer_c = request.form.get("answer_c", "")
        answer_d = request.form.get("answer_d", "")
        correct_answer = request.form.get("correct_answer")
        if not question.strip() or not answer_a.strip() or not answer_b.strip() or not answer_c.strip() or not answer_d.strip():
            return render_template("add_question.html", quiz_id=quiz_id, question=question, answer_a=answer_a, answer_b=answer_b, answer_c=answer_c, answer_d=answer_d, correct_answer=correct_answer, error="All fields are required")
        if correct_answer not in ["A", "B", "C", "D"]:
            return render_template("add_question.html", quiz_id=quiz_id, question=question, answer_a=answer_a, answer_b=answer_b, answer_c=answer_c, answer_d=answer_d, correct_answer=correct_answer, error="Invalid correct answer")
        save_question(quiz_id, question, answer_a, answer_b, answer_c, answer_d, correct_answer)
        return redirect(url_for("view_quiz", quiz_id=quiz_id))
    return render_template("add_question.html", quiz_id=quiz_id)

@app.route("/quiz/<int:quiz_id>/take-quiz", methods=["GET", "POST"])
def take_quiz(quiz_id):
    quiz = get_quiz(quiz_id)
    if not quiz:
        abort(404)
    questions = get_questions(quiz_id)
    if not questions:
        return redirect(url_for("view_quiz", quiz_id=quiz_id))
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
    question = get_question(question_id)
    if not question:
        abort(404)
    if question[1] != quiz_id:
        abort(404)
    delete_question(question_id)
    return redirect(url_for("view_quiz", quiz_id=quiz_id))

@app.route("/quiz/<int:quiz_id>/question/<int:question_id>/edit", methods=["GET", "POST"])
def edit_question_route(quiz_id, question_id):
    question = get_question(question_id)
    if not question:
        abort(404)
    if question[1] != quiz_id:
        abort(404)
    if request.method == "POST":
        question_text = request.form.get("question", "")
        answer_a = request.form.get("answer_a", "")
        answer_b = request.form.get("answer_b", "")
        answer_c = request.form.get("answer_c", "")
        answer_d = request.form.get("answer_d", "")
        correct_answer = request.form.get("correct_answer")
        if not question_text.strip() or not answer_a.strip() or not answer_b.strip() or not answer_c.strip() or not answer_d.strip():
            return render_template("edit_question.html", question=question, question_text=question_text, answer_a=answer_a, answer_b=answer_b, answer_c=answer_c, answer_d=answer_d, correct_answer=correct_answer, error="All fields are required")
        if correct_answer not in ["A", "B", "C", "D"]:
            return render_template("edit_question.html", question=question, question_text=question_text, answer_a=answer_a, answer_b=answer_b, answer_c=answer_c, answer_d=answer_d, correct_answer=correct_answer, error="Invalid correct answer")
        update_question(question_id, question_text, answer_a, answer_b, answer_c, answer_d, correct_answer)
        return redirect(url_for("view_quiz", quiz_id=quiz_id))
    return render_template("edit_question.html", question=question)

@app.route("/quiz/<int:quiz_id>/edit", methods=["GET", "POST"])
def edit_quiz(quiz_id):
    quiz = get_quiz(quiz_id)
    if not quiz:
        abort(404)
    if request.method == "POST":
        quiz_name = request.form.get("quiz_name", "")
        if not quiz_name.strip():
            return render_template("edit_quiz.html", quiz=quiz, quiz_name=quiz_name, error="Quiz name is required")
        update_quiz(quiz_id, quiz_name)
        return redirect(url_for("view_quiz", quiz_id=quiz_id))
    return render_template("edit_quiz.html", quiz=quiz)

@app.route("/quiz/<int:quiz_id>/delete", methods=["POST"])
def delete_quiz_route(quiz_id):
    quiz = get_quiz(quiz_id)
    if not quiz:
        abort(404)
    delete_quiz(quiz_id)
    return redirect(url_for("welcome"))

if __name__ == "__main__":
    app.run(debug=True)