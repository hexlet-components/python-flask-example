import json
import uuid
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

users = json.load(open("./users.json", 'r'))


@app.route('/')
def index():
    return 'Welcome to Flask!'


@app.route('/users/')
def users_get():
    with open("./users.json", "r") as f:
        users = json.load(f)
    term = request.args.get('term', '')
    filtered_users = [user for user in users if term in user['name']]
    return render_template(
        'users/index.html',
        users=filtered_users,
        search=term,
    )


@app.post('/users')
def users_post():
    user_data = request.form.to_dict()
    errors = validate(user_data)
    if errors:
        return render_template(
            'users/new.html',
            user=user_data,
            errors=errors,
        )
    id = str(uuid.uuid4())
    user = {
        'id': id,
        'name': user_data['name'],
        'email': user_data['email']
    }
    users.append(user)
    with open("./users.json", "w") as f:
        json.dump(users, f)
    return redirect(url_for('users_get'), code=302)


@app.route('/users/new')
def users_new():
    user = {'name': '', 'email': ''}
    errors = {}
    return render_template(
        'users/new.html',
        user=user,
        errors=errors,
    )


@app.route('/users/<id>')
def show_user(id):
    with open("./users.json", "r") as f:
        users = json.load(f)
    user = next(user for user in users if id == str(user['id']))
    return render_template(
        'users/show.html',
        user=user,
    )


@app.route('/courses/<id>')
def courses(id):
    return f'Course id: {id}'


def validate(user):
    errors = {}
    if not user['name']:
        errors['name'] = "Can't be blank"
    if not user['email']:
        errors['email'] = "Can't be blank"
    return errors
