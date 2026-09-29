# Quiz Generator

Quiz Generator is a web application built with Python and Flask that allows users to create and manage custom multiple-choice quizzes. Users can add questions and answers, choose the correct answer, take their quizzes, and receive their score when finished.

I built this project to practice full-stack web development concepts including Flask routing, HTML forms, SQLite databases, CRUD operations, form validation, and responsive CSS.

## Features

- Create custom quizzes
- Edit quiz names
- Delete quizzes
- Add multiple-choice questions
- Edit existing questions and answers
- Delete questions
- Choose the correct answer for each question
- Take completed quizzes
- Automatically calculate quiz scores
- Review correct and incorrect answers
- Retake quizzes
- Form validation
- Confirmation before deleting quizzes or questions
- Error handling for invalid quiz and question URLs
- Responsive design for desktop and mobile devices

## Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- Jinja
- Git and GitHub

## Project Structure

```text
Quiz_Generator/
│
├── app.py
├── storage.py
├── static/
│   └── style.css
├── templates/
│   ├── index.html
│   ├── create_quiz.html
│   ├── view_quiz.html
│   ├── edit_quiz.html
│   ├── add_question.html
│   ├── edit_question.html
│   ├── take_quiz.html
│   └── results.html
└── README.md