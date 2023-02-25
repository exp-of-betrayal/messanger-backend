from configs.registration_patterns import email_pattern, nickname_pattern, password_pattern
from flask import Flask, render_template, request
import re

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route('/')
def index():
    return "you are in main page <a href='/login'>login</a>, <a href='/registration'>reg</a>"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        return "post to login"
    return render_template("account.html")


def verify_reg(name, email, password):
    errors = []
    print(name, email, password)
    if not(4 <= len(name) <= 16):
        errors.append([1, "Nickname length must be from 4 to 12 characters"])
    if not bool(re.match(nickname_pattern, str(name))):
        errors.append([1, "Nickname incorrect"])
    if not bool(re.match(email_pattern, str(email))):
        errors.append([2, "E-mail incorrect"])
    if not bool(re.match(password_pattern, str(password))):
        errors.append([3, "Password incorrect"])
    print(f"errors -> {errors}")
    if not errors:
        return 0
    else:
        return errors


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == "POST":
        print(request.form.values())
        name = request.form.get("nickname")
        email = request.form.get("email")
        password = request.form.get("password")
        errors = verify_reg(name, email, password)
        if not errors:
            return "succesfull registration"
        else:
            return render_template("registration.html", errors=errors, values=[name, email, password])

    return render_template("registration.html")


app.run()
