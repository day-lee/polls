# How to Install the "Polls" (Project 설치 방법)
```
# Create a New Directory for the Project
mkdir project_name

# Create a Virtual Environment
cd project_name
python -m venv venv

# Activate the Virtual Enviroment on terminal
source project_name\venv\Scripts\activate
if this "(venv)" shows up, virtual environment has been successfully created

# Install Required Packages
pip install -r requirements.txt

# Add secrets.json file at a same level where manage.py file exists
#for SECRET_KEY value at settings.py

# (optional) Migrate Tables
-> this step can be skipped as sqlite3 db is already included  in this repo, however,
if you want to start from scratch, run this command
python manage.py makemigrations
python manage.py migrate

# Create Admin Account
python manage.py createsuperuser

# Run Server
python manage.py runserver


* Dummy sqlite3 database is included in this project for educational purpose
	학습용 프로젝트로 sqlite3 DATABASE를 참고할 수 있도록 레포지토리에 추가해두었습니다.
```

# TODO
1.  [x] Raise 404 if no matching question
2.  [x] Show only questions that are published and not yet closed
3.  [x] Enable to comment on question
4.  [ ] Enable to comment on comment
5.  [x] Enable to suggest new choice for question
6.  [x] Limit the number of choices that can be suggested on one question
7.  [ ] Extends `Question.closed_at` by one day, when new choice is suggested for that question
     - Requirements:
         - Use Django signal/receiver system
8.  [ ] In `/polls/`, fetch only 5 questions through REST API
9.  [x] Handle race condition on handling "vote" action
10. [x] Implement login system
11. [ ] Implement system that a question creator can approve suggested choices
12. [x] Implement global search for questions and choices


