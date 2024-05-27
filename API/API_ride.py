import psycopg2
from psycopg2 import sql
from datetime import datetime


class RideTable:
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

    def passenger_board(self, passenger_id, start_station):
        try:
            unfinished = self.query_unfinished_passenger_rides()
            for passenger in unfinished:
                if passenger[0] == str(passenger_id):
                    print("Error: This passenger has not been finished last ride! ")
                    return
            start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            self.cursor.execute(sql.SQL("SELECT setval('passenger_ride_passenger_ride_id_seq', "
                                        "(SELECT MAX(passenger_ride_id) FROM passenger_ride))"))
            self.cursor.execute(
                sql.SQL(
                    "INSERT INTO passenger_ride (passenger_id, start_station, end_station, price, start_time, end_time)"
                    " VALUES (%s, %s, NULL, 0, %s, NULL)"),
                [passenger_id, start_station, start_time]
            )
            self.connection.commit()
            print("Passenger boarded successfully.")
        except Exception as e:
            self.connection.rollback()
            print(f"Error boarding passenger: {e}")

    def passenger_alight(self, passenger_id, start_station, end_station):
        try:
            unfinished = self.query_unfinished_passenger_rides()
            for passenger in unfinished:
                if passenger[0] == str(passenger_id):
                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                    price = self.get_price(start_station, end_station)[0][0]
                    self.cursor.execute(
                        sql.SQL(
                            "UPDATE passenger_ride SET end_station = %s, end_time = %s, price = %s "
                            "WHERE passenger_id = %s AND end_time IS NULL"),
                        [end_station, end_time, price, str(passenger_id)]
                    )
                    self.connection.commit()
                    print("Passenger alighted successfully.")
                    return
            print("Error: Passenger has not been boarded! ")
        except Exception as e:
            self.connection.rollback()
            print(f"Error alighting passenger: {e}")

    def card_board(self, card_code, start_station):
        try:
            unfinished = self.query_unfinished_card_rides()
            for passenger in unfinished:
                if passenger[0] == card_code:
                    print("Error: This card has not been finished last ride! ")
                    return
            start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            self.cursor.execute(sql.SQL("SELECT setval('card_ride_card_ride_id_seq', "
                                        "(SELECT MAX(card_ride_id) FROM card_ride))"))
            self.cursor.execute(
                sql.SQL(
                    "INSERT INTO card_ride (card_code, start_station, end_station, price, start_time, end_time) "
                    "VALUES (%s, %s, NULL, 0, %s, NULL)"),
                [card_code, start_station, start_time]
            )
            self.connection.commit()
            print("Card boarded successfully.")
        except Exception as e:
            self.connection.rollback()
            print(f"Error boarding card: {e}")

    def card_alight(self, card_code, start_station, end_station):
        try:
            unfinished = self.query_unfinished_card_rides()
            for passenger in unfinished:
                if passenger[0] == card_code:
                    price = self.get_price(start_station, end_station)[0][0]
                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                    self.cursor.execute(
                        sql.SQL(
                            "UPDATE card_ride SET end_station = %s, end_time = %s, price = %s "
                            "WHERE card_code = %s AND end_time IS NULL"),
                        [end_station, end_time, price, card_code]
                    )
                    self.cursor.execute(
                        sql.SQL(
                            "UPDATE cards SET money = money - %s WHERE code = %s"), [price, card_code])
                    self.cursor.execute(
                        sql.SQL(
                            "SELECT money FROM cards WHERE code = %s"), [card_code])
                    money = self.cursor.fetchone()[0]
                    if money < 0:
                        print("Error: This card does not have enough money! "
                              "Please go to the Customer Service Center for help! ")
                        return
                    self.connection.commit()
                    print("Card alighted successfully.\nAccount Balance: " + str(money))
                    if money < 10:
                        print("Warning: This card has less than 10 RMB! ")
                    return
            print("Error: Card has not been boarded! ")
        except Exception as e:
            self.connection.rollback()
            print(f"Error alighting card: {e}")

    def query_unfinished_passenger_rides(self):
        try:
            self.cursor.execute(
                sql.SQL("SELECT passenger_id, start_station, start_time FROM passenger_ride WHERE end_time IS NULL")
            )
            unfinished_passenger_rides = self.cursor.fetchall()

            return unfinished_passenger_rides
        except Exception as e:
            print(f"Error querying unfinished rides: {e}")
            return None, None

    def query_unfinished_card_rides(self):
        try:
            self.cursor.execute(
                sql.SQL("SELECT card_code, start_station, start_time FROM card_ride WHERE end_time IS NULL")
            )
            unfinished_card_rides = self.cursor.fetchall()

            return unfinished_card_rides
        except Exception as e:
            print(f"Error querying unfinished rides: {e}")
            return None, None

    def get_price(self, start_station, end_station):
        self.cursor.execute(sql.SQL(
            "SELECT DISTINCT price FROM (SELECT end_station_id, price.price FROM price "
            "JOIN stations ON start_station_id = stations.station_id "
            "WHERE english_name = %s) as t "
            "JOIN stations ON end_station_id = stations.station_id "
            "WHERE english_name = %s"
        ), [start_station, end_station])
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()
