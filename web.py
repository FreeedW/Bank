from flask import Flask, render_template, redirect, url_for, request, flash
from db import *

app = Flask(__name__)
app.secret_key = "your-secret-key-here"

db = DataBase()


@app.route("/")
def home():
    return render_template("base.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        # Создаем пользователя в БД
        db.create_users_db(username)
        # Получаем сгенерированный пасскод
        user = db.get_condition_db("users", f"username = '{username}'")[0]
        secret_key = user[2]  # Получаем secret_key из результата запроса
        # Показываем пасскод пользователю
        flash(secret_key)
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        passcode = request.form["passcode"]
        print(f"Попытка входа: {username}, {passcode}")
        if db.login_user(username, passcode):
            print("ОК")
        else:
            print("NO OK")
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
