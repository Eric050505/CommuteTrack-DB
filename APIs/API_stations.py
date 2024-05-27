import psycopg2
from psycopg2 import sql


class StationTable:
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

    def add_station(self, chinese_name, english_name, district, intro):
        try:
            self.cursor.execute(sql.SQL("SELECT setval('stations_station_id_seq', "
                                        "(SELECT MAX(station_id) FROM stations))"))
            self.cursor.execute(
                sql.SQL(
                    "INSERT INTO stations "
                    "(chinese_name, english_name, district, intro) VALUES (%s, %s, %s, %s)"),
                [chinese_name, english_name, district, intro]
            )
            self.connection.commit()
            print("Station " + english_name + " added successfully.")
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding station: {e}")

    def modify_station(self, station_id, chinese_name=None, english_name=None, district=None, intro=None):
        try:
            query = sql.SQL("UPDATE stations SET ")
            updates = []
            params = []
            if chinese_name is not None:
                updates.append(sql.SQL("chinese_name = %s"))
                params.append(chinese_name)
            if english_name is not None:
                updates.append(sql.SQL("english_name = %s"))
                params.append(english_name)
            if district is not None:
                updates.append(sql.SQL("district = %s"))
                params.append(district)
            if intro is not None:
                updates.append(sql.SQL("intro = %s"))
                params.append(intro)

            if not updates:
                print("No fields to update.")
                return

            query += sql.SQL(", ").join(updates) + sql.SQL(" WHERE station_id = %s")
            params.append(station_id)
            self.cursor.execute(query, params)
            self.connection.commit()
            print("Station modified successfully.")
        except Exception as e:
            self.connection.rollback()
            print(f"Error modifying station: {e}")

    def delete_station(self, station_id):
        try:
            self.cursor.execute(sql.SQL("SELECT english_name from stations WHERE station_id = %s"), [station_id])
            english_name = self.cursor.fetchall()
            english_name = english_name[0][0]
            self.cursor.execute(
                sql.SQL("DELETE FROM stations WHERE station_id = %s"),
                [station_id]
            )
            self.connection.commit()
            print("Station" + english_name + "deleted successfully.")
        except Exception as e:
            self.connection.rollback()
            print(f"Error deleting station: {e}")

    def close(self):
        self.cursor.close()
        self.connection.close()
