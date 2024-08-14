from flask import Flask, render_template

app = Flask(__name__)

users = ['mike', 'mishel', 'adel', 'keks', 'kamila']


@app.route('/')
def hello_world():
    return 'Welcome to Flask!'


@app.get('/users')
def users_get():
    return 'GET /users'


@app.post('/users')
def users():
    return 'Users', 302


@app.route('/courses/<id>')
def courses(id):
    return f'Course id: {id}'


@app.route('/users/<id>')
def show_user(id):
    user = {
        "id": id,
        "name": f"user-{id}"
    }
    return render_template(
        'users/show.html',
        user=user,
    )
