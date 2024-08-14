import json
import sys
import uuid

class UserRepository:
    def __init__(self):
        self.users = json.load(open("./users.json", 'r'))

    def get_content(self):
        return self.users

    def find(self, id):
        try:
            for user in self.users:
                if str(id) == str(user['id']):
                    return user
        except KeyError:
            sys.stderr.write(f'Wrong post id: {id}')
            raise

    def save(self, user_data):
        # repository should know nothing about validation in outer layer
        if not (user_data.get('name') and user_data.get('email')):
            raise Exception(f'Wrong data: {json.dumps(user_data)}')

        if 'id' not in user_data:
            new_user = user_data.copy()
            new_user['id'] = str(uuid.uuid4())
            self.users.append(new_user)
        else:
            for i, existing_user in enumerate(self.users):
                if str(user_data['id']) == str(existing_user['id']):
                    self.users[i] = user_data
                    break
            else:
                raise Exception(f"User with id {user_data['id']} not found")

        with open("./users.json", "w") as f:
            json.dump(self.users, f)

        return user_data['id']

    def destroy(self, id):
        current_user = self.find(id)
        self.users.remove(current_user)
        with open("./users.json", "w") as f:
            json.dump(self.users, f)
