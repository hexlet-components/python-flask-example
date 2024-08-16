from psycopg2.extras import RealDictCursor


class UserRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_content(self):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM users")
            return cur.fetchall()

    def get_by_term(self, search_term=''):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE name ILIKE %s", (f'%{search_term}%',))
            return cur.fetchall()

    def find(self, id):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (id,))
            return cur.fetchone()

    def save(self, user_data):
        if 'id' not in user_data:
            id = self._create(user_data)
        else:
            id = self._update(user_data)
        return id


    def _update(self, user_data):
        with self.conn.cursor() as cur:
            cur.execute(
                    "UPDATE users SET name = %s, email = %s WHERE id = %s",
                    (user_data['name'], user_data['email'], user_data['id'])
                )
        self.conn.commit()
        return user_data['id']


    def _create(self, user_data):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id",
                (user_data['name'], user_data['email'])
            )
            user_data['id'] = cur.fetchone()[0]
        self.conn.commit()
        return user_data['id']


    def destroy(self, id):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s", (id,))
        self.conn.commit()
