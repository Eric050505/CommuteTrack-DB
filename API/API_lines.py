import psycopg2
from psycopg2 import sql


class LinesTable:
    def __init__(self, database, user, password, host, port):
        self.connection = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute("SET search_path TO project")

    def add_line(self, chinese_name, start_time, end_time, mileage, color, first_opening, intro, url):
        try:
            self.cursor.execute(sql.SQL("SELECT setval('lines_line_id_seq', (SELECT MAX(line_id) FROM lines))"))
            self.cursor.execute(
                sql.SQL(
                    "INSERT INTO lines "
                    "(Chinese_name, start_time, end_time, mileage, color, first_opening, intro, url) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"),
                [chinese_name, start_time, end_time, mileage, color, first_opening, intro, url]
            )
            self.connection.commit()
            print("Line" + chinese_name + "added successfully.")
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding line: {e}")

    def modify_line(self, line_id, chinese_name=None, start_time=None, end_time=None, mileage=None, color=None,
                    first_opening=None, intro=None, url=None):
        try:
            query = sql.SQL("UPDATE lines SET ")
            updates = []
            params = []
            if chinese_name is not None:
                updates.append(sql.SQL("Chinese_name = %s"))
                params.append(chinese_name)
            if start_time is not None:
                updates.append(sql.SQL("start_time = %s"))
                params.append(start_time)
            if end_time is not None:
                updates.append(sql.SQL("end_time = %s"))
                params.append(end_time)
            if mileage is not None:
                updates.append(sql.SQL("mileage = %s"))
                params.append(mileage)
            if color is not None:
                updates.append(sql.SQL("color = %s"))
                params.append(color)
            if first_opening is not None:
                updates.append(sql.SQL("first_opening = %s"))
                params.append(first_opening)
            if intro is not None:
                updates.append(sql.SQL("intro = %s"))
                params.append(intro)
            if url is not None:
                updates.append(sql.SQL("url = %s"))
                params.append(url)

            if not updates:
                print("No fields to update.")
                return

            query += sql.SQL(", ").join(updates) + sql.SQL(" WHERE line_id = %s")
            params.append(line_id)
            self.cursor.execute(query, params)
            self.connection.commit()
            print("Line" + chinese_name + "modified successfully.")
        except Exception as e:
            self.connection.rollback()
            print(f"Error modifying line: {e}")

    def delete_line(self, line_id):
        try:
            self.cursor.execute(sql.SQL("SELECT chinese_name from lines WHERE line_id = %s"), [line_id])
            chinese_name = str(self.cursor.fetchone())
            self.cursor.execute(
                sql.SQL("DELETE FROM lines WHERE line_id = %s"),
                [line_id]
            )
            self.connection.commit()
            print("Line" + chinese_name + "added successfully.")
        except Exception as e:
            self.connection.rollback()
            print(f"Error deleting line: {e}")

    def close(self):
        self.cursor.close()
        self.connection.close()
