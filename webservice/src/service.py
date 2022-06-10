from logging import LoggerAdapter
import db_interface
import initialize_data
from flask import Flask, redirect, render_template, request, url_for, g

db = db_interface.DBHandle()

initialize_data.insert(db.users)

app = Flask(__name__)

current_user = None


@app.route('/auth/login/', methods=['POST', "GET"])
def login():
    global current_user
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        current_user = db.find_user(username, password)
        if current_user == None:
            return render_template("login.html", login_failed=True)
        return redirect(url_for("homepage", username=current_user['username']))
    else:
        return render_template("login.html", login_failed=None)


@app.route('/auth/register/<admin>', methods=['POST', "GET"])
def register(admin):
    global current_user
    admin_bool = admin == 'True'

    if admin_bool and not current_user["admin"]:
        return redirect(url_for("register", admin=False))

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        password = request.form.get("password")

        if db.find_user(username, password) is not None or db.find_user(email, password) is not None:
            return render_template("register.html", user_exists=True)

        new_user = {"admin": admin_bool, "username": username, "email": email,
                    "first_name": first_name, "last_name": last_name, "password": password}
        db.users.insert_one(new_user)

        if not admin_bool:
            current_user = new_user
        return redirect(url_for("homepage", username=current_user['username']))
    else:
        return render_template("register.html", admin=admin_bool)


@app.route('/auth/logout/')
def logout():
    global current_user
    current_user = None
    return redirect(url_for("homepage"))


@app.route('/index/<username>/')
@app.route('/index/')
def homepage(username=None):
    if username is None:
        if current_user is not None:
            return redirect(url_for("homepage", username=current_user["username"]))
        return render_template("index.html")
    if current_user is None or username != current_user["username"]:
        return redirect(url_for("login"))
    return render_template("index.html", current_user=current_user)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
