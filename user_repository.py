import psycopg2
from psycopg2.extras import RealDictCursor


class UserRepository:
    def __init__(self, db_url):
        self.db_url = db_url

    def get_connection(self):
        return psycopg2.connect(self.db_url)

    def get_content(self):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM users")
                return cur.fetchall()

    def find(self, id):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM users WHERE id = %s", (id,))
                return cur.fetchone()

    def save(self, user_data):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                if 'id' not in user_data:
                    # New user
                    cur.execute(
                        "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id",
                        (user_data['name'], user_data['email'])
                    )
                    user_data['id'] = cur.fetchone()[0]
                else:
                    # Existing user
                    cur.execute(
                        "UPDATE users SET name = %s, email = %s WHERE id = %s",
                        (user_data['name'], user_data['email'], user_data['id'])
                    )
            conn.commit()
        return user_data['id']

    def destroy(self, id):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE id = %s", (id,))
            conn.commit()
