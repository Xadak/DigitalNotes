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
        current_user = db.find_user_by_username(username, password)
        if current_user == None:
            return render_template("login.html", login_failed=True)
        return redirect(url_for("homepage", username=current_user['username']))
    else:
        return render_template("login.html", login_failed=None)


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
