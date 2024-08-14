from flask import Flask, render_template, request

app = Flask(__name__)

users = [
    {'id': 1, 'name': 'mike'},
    {'id': 2, 'name': 'mishel'},
    {'id': 3, 'name': 'adel'},
    {'id': 4, 'name': 'keks'},
    {'id': 5, 'name': 'kamila'}
]


@app.route('/')
def hello_world():
    return 'Welcome to Flask!'


@app.route('/users/')
def get_users():
    term = request.args.get('term', '')
    print(users)
    filtered_users = [user for user in users if term in user['name']]
    return render_template(
        'users/index.html',
        users=filtered_users,
        search=term,
    )


@app.post('/users')
def post_users():
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
