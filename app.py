from configs.registration_patterns import email_pattern, nickname_pattern, password_pattern
from flask import Flask, render_template, request, make_response, redirect
import re
import databases as db

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route('/')
def index():
    # attention! code when will be ниже mast be deleted
    resp = make_response("you are in main page <a href='/login'>login</a>, <a href='/registration'>reg</a>")
    resp.set_cookie('token', '', 60 * 60 * 24)
    resp.set_cookie('id', '', 60 * 60 * 24)
    # it use for clearing cookie
    # return "you are in main page <a href='/login'>login</a>, <a href='/registration'>reg</a>"
    return resp


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.cookies.get('token'):
        id = int(request.cookies.get('id'))
        token = request.cookies.get('token')
        if db.check_token(int(id), token) == 0:
            return redirect('/me')
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        valid = db.data_correctly(email, password)
        if valid == -1:
            return render_template("account.html", error_log="email didn't registry yet")
        elif valid == 0:
            response = make_response(redirect("/me"))
            id = db.get_id_by_email(email=email)
            token = db.generate_token()
            print(f"id->{id},token->{token}.")
            response.set_cookie('token', token, 60 * 60 * 24)
            response.set_cookie('id', str(id), 60 * 60 * 24)
            return response
        else:
            return render_template("account.html", error_log="password or email incorrect")
    return render_template("account.html")


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.cookies.get('token'):
        id = int(request.cookies.get('id'))
        token = request.cookies.get('token')
        if db.check_token(int(id), token) == 0:
            return redirect('/me')
    if request.method == "POST":
        name = request.form.get("nickname")
        email = request.form.get("email")
        password = request.form.get("password")

        errors = verify_reg(name, email, password)
        if not errors:
            token, user_id = db.registry_new_acc(username=name, password=password, email=email)
            res = make_response(redirect("me"))
            res.set_cookie('token', str(token), max_age=60 * 60 * 24)
            res.set_cookie('id', str(user_id), max_age=60 * 60 * 24)
            return res
        else:
            return render_template("registration.html", errors=errors, values=[name, email, password])

    return render_template("registration.html")


@app.route('/me', methods=['GET', 'POST'])
def user_page():
    if not request.cookies.get('token'):
        return redirect("/login")
    else:
        token = request.cookies.get('token')
        id = request.cookies.get('id')
        if db.check_token(int(id), token):
            resp = make_response(redirect("/login"))
            resp.set_cookie('token', '', 60 * 60 * 24)
            resp.set_cookie('id', '', 60 * 60 * 24)
        else:
            return "Ну типо вы авторизованы (типо)"


@app.route('/forgot-password')
def forgot():
    return redirect('https://yandex.ru/images/search?from=tabbar&text=%D0%B3%D0%BB%D0%B8%D1%86%D0%B8%D0%BD%20%D1%80%D0%B5%D0%BA%D0%BB%D0%B0%D0%BC%D0%B0')


def verify_reg(name, email, password):
    errors = []
    print(name, email, password)
    if not(4 <= len(name) <= 16):
        errors.append([1, "Nickname length must be from 4 to 12 characters"])
    if not bool(re.match(nickname_pattern, str(name))):
        errors.append([1, "Nickname incorrect"])
    if db.is_mail_registry(email):
        errors.append([2, "E-mail already used"])
    if not bool(re.match(email_pattern, str(email))):
        errors.append([2, "E-mail incorrect"])
    if not bool(re.match(password_pattern, str(password))):
        errors.append([3, "Password incorrect"])
    print(f"errors -> {errors}")
    if not errors:
        return 0
    else:
        return errors


app.run()
