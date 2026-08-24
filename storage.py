import sqlite3

def get_db_connection():
    connection = sqlite3.connect("database.db")
    return connection

def initialize_database():
    connection = get_db_connection()
    connection.execute("""
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY,
            name TEXT
            )
        """)
    connection.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY,
                quiz_id INTEGER,
                question TEXT,
                answer_a TEXT,
                answer_b TEXT,
                answer_c TEXT,
                answer_d TEXT,
                correct_answer TEXT
                )
            """)
    connection.commit()
    connection.close()

def save_quiz(quiz_name):
    connection = get_db_connection()
    connection.execute(
        "INSERT INTO quizzes (name) VALUES (?)",
        (quiz_name,)
    )
    connection.commit()
    connection.close()

def save_question(quiz_id, question, answer_a, answer_b, answer_c, answer_d, correct_answer):
    connection = get_db_connection()
    connection.execute(
        "INSERT INTO questions (quiz_id, question, answer_a, answer_b, answer_c, answer_d, correct_answer) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (quiz_id, question, answer_a, answer_b, answer_c, answer_d, correct_answer)
    )
    connection.commit()
    connection.close()

def get_quizzes():
    connection = get_db_connection()
    quizzes = connection.execute(
        "SELECT * FROM quizzes"
    ).fetchall()
    connection.close()
    return quizzes

def get_quiz(quiz_id):
    connection = get_db_connection()
    quiz = connection.execute(
        "SELECT * FROM quizzes WHERE id = ?",
        (quiz_id,)
    ).fetchone()
    connection.close()
    return quiz

def get_questions(quiz_id):
    connection = get_db_connection()
    questions = connection.execute(
        "SELECT * FROM questions WHERE quiz_id = ?",
        (quiz_id,)
    ).fetchall()
    connection.close()
    return questions

def delete_question(question_id):
    connection = get_db_connection()
    connection.execute(
        "DELETE FROM questions WHERE id = ?",
        (question_id,)
    )
    connection.commit()
    connection.close()