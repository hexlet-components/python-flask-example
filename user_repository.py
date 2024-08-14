import json
import sys
import uuid
from flask import session


class UserRepository():
    def __init__(self):
        if 'user' not in session:
            session['user'] = {}

    def get_content(self):
        return session['user'].values()

    def find(self, id):
        try:
            return session['user'][id]
        except KeyError:
            sys.stderr.write(f'Wrong user id: {id}')
            raise

    def destroy(self, id):
        del session['user'][id]

    def save(self, user):
        if not (user.get('name') and user.get('email')):
            raise Exception(f'Wrong data: {json.loads(user)}')
        if not user.get('id'):
            user['id'] = str(uuid.uuid4())
        session['user'][user['id']] = user
        session['user'] = session['user']
        return user['id']
