import psycopg2
from psycopg2 import sql


class LinesDetailTable:
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

    def place_new_stations(self, line_id, stations):
        try:
            for station in stations:
                station_id = station['station_id']
                position = station['nums']
                self.cursor.execute(
                    sql.SQL("UPDATE lines_detail SET nums = nums + 1 WHERE line_id = %s AND nums >= %s"),
                    [line_id, position]
                )
                self.cursor.execute(
                    sql.SQL("INSERT INTO lines_detail (line_id, station_id, nums) VALUES (%s, %s, %s)"),
                    [line_id, station_id, position]
                )
                self.connection.commit()
                print("Stations placed in line successfully.")
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding line: {e}")

    def remove_station_in_line(self, line_id, station_id):
        try:
            self.cursor.execute(
                sql.SQL("SELECT nums FROM lines_detail WHERE line_id = %s AND station_id = %s"),
                [line_id, station_id]
            )
            result = self.cursor.fetchone()
            if result:
                position = result[0]
                self.cursor.execute(
                    sql.SQL("DELETE FROM lines_detail WHERE line_id = %s AND station_id = %s"),
                    [line_id, station_id]
                )
                self.cursor.execute(
                    sql.SQL("UPDATE lines_detail SET nums = nums - 1 WHERE line_id = %s AND nums > %s"),
                    [line_id, position]
                )
                self.connection.commit()
                print("Station removed from line successfully.")
            else:
                print("Station or line not found OR station not contained in line.")
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding line: {e}")

    def close(self):
        self.cursor.close()
        self.connection.close()
