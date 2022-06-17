from logging import LoggerAdapter
from datetime import datetime
import db_interface
import initialize_data
from flask import Flask, redirect, render_template, request, url_for, g
from flask_objectid_converter import ObjectIDConverter

db = db_interface.DBHandle()

initialize_data.insert(db.users)

app = Flask(__name__)
app.url_map.converters['objectid'] = ObjectIDConverter

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


@app.route('/delete_self/')
def delete_self():
    global current_user
    if current_user is not None:
        db.delete_user(current_user["username"])
        current_user = None
    return redirect(url_for("homepage"))


@app.route('/delete_other/', methods=['POST', 'GET'])
def delete_other():
    global current_user
    if current_user is None or not current_user["admin"]:
        return redirect(url_for("homepage"))

    if request.method == "POST":
        username = request.form.get("username")

        if username != current_user["username"]:
            if db.delete_user(username) is None:
                return render_template("delete_user.html", not_found=True, username=current_user["username"])
            return redirect(url_for("homepage"))
        return render_template("delete_user.html", selected_self=True, username=current_user["username"])
    return render_template("delete_user.html", username=current_user["username"])


@app.route('/index/<username>/', methods=["POST", "GET"])
@app.route('/index/<username>/<descending>/', methods=["POST", "GET"])
@app.route('/index/')
def homepage(username=None, descending=None):
    search_text = None
    search_tag = None
    if request.method == 'POST':
        search_text = request.form.get('search')
        search_tag = request.form.get('search_tag')

    if username is None:
        if current_user is not None:
            return redirect(url_for("homepage", username=current_user["username"], descending=descending))
        return render_template("index.html")
    if current_user is None or username != current_user["username"]:
        return redirect(url_for("login"))
    return render_template("index.html", current_user=current_user, descending=descending,
                           notes=[note for note in sorted(db.notes_of(current_user["_id"]), key=lambda x: x['date'], reverse=descending is not None)
                                  if note['title'].startswith(search_text if search_text else "") and (search_tag in note['tags'] if search_tag else True)])


@app.route('/create_note', methods=["POST", "GET"])
def create_note():
    if current_user is None:
        return redirect(url_for("login"))

    if request.method == "POST":
        user_id = current_user["_id"]
        title = request.form.get("title")
        creation_date = datetime.now()
        content = request.form.get("content").lstrip(' ')
        tags = [tag.lstrip(' ').rstrip(' ')
                for tag in str.split(request.form.get("tags"), ",")]

        db.add_note(user_id, title, creation_date, content, tags)
        return redirect(url_for('homepage'))

    return render_template("create_note.html", current_user=current_user)


@app.route('/delete_note/<objectid:user_id>/<objectid:note_id>/')
def delete_note(user_id, note_id):
    if current_user is None or current_user['_id'] != user_id:
        return redirect(url_for("homepage"))
    db.delete_note(user_id, note_id)
    return redirect(url_for("homepage"))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
