import json
import sys
import uuid

class UserRepository():
    def __init__(self):
        self.users = json.load(open("./users.json", 'r'))

    def get_content(self):
        return self.users

    def find(self, id):
        try:
            for user in self.users:
                if id == str(user['id']):
                    return user
        except KeyError:
            sys.stderr.write(f'Wrong post id: {id}')
            raise

    def save(self, new_user):
        # repository should know nothing about validation in outer layer
        if not (new_user.get('name') and new_user.get('email')):
            raise Exception(f'Wrong data: {json.loads(new_user)}')
        # replace already existed user
        if new_user.get('id'):
            current_user = self.find(new_user['id'])
            self.users.pop(current_user)
            self.users.append(new_user)
        # or add new
        else:
            new_user['id'] = str(uuid.uuid4())
            self.users.append(new_user)
        with open("./users.json", "w") as f:
            json.dump(self.users, f)
        return new_user['id']
