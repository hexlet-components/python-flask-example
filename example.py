from flask import (
    get_flashed_messages,
    flash,
    Flask,
    redirect,
    render_template,
    request,
    url_for
)
from user_repository import UserRepository

app = Flask(__name__)
app.secret_key = "secret_key"


@app.route('/')
def index():
    return 'Welcome to Flask!'


@app.route('/users/')
def users_get():
    messages = get_flashed_messages(with_categories=True)
    term = request.args.get('term', '')
    repo = UserRepository()
    users = repo.get_content()
    filtered_users = [user for user in users if term in user['name']]
    return render_template(
        'users/index.html',
        users=filtered_users,
        search=term,
        messages=messages
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
    repo = UserRepository()
    repo.save(user_data)

    flash('Пользователь успешно добавлен', 'success')
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


@app.route('/users/<id>/edit')
def users_edit(id):
    repo = UserRepository()
    user = repo.find(id)
    errors = {}

    return render_template(
        'users/edit.html',
        user=user,
        errors=errors,
    )


@app.route('/users/<id>/patch', methods=['POST'])
def users_patch(id):
    repo = UserRepository()
    user = repo.find(id)
    data = request.form.to_dict()

    errors = validate(data)
    if errors:
        return render_template(
            'users/edit.html',
            user=user,
            errors=errors,
        ), 422
    data['id'] = user['id']
    repo.save(data)
    flash('Пользователь успешно обновлен', 'success')
    return redirect(url_for('users_get'))


@app.route('/users/<id>/delete', methods=['POST'])
def users_delete(id):
    repo = UserRepository()
    repo.destroy(id)
    flash('Пользователь удален', 'success')
    return redirect(url_for('users_get'))


@app.route('/users/<id>')
def users_show(id):
    repo = UserRepository()
    user = repo.find(id)
    return render_template(
        'users/show.html',
        user=user,
    )


def validate(user):
    errors = {}
    if not user['name']:
        errors['name'] = "Can't be blank"
    if not user['email']:
        errors['email'] = "Can't be blank"
    return errors
