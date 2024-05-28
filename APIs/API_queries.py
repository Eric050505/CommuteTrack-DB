import heapq
from collections import defaultdict

import psycopg2
from psycopg2 import sql


class Queries:
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
        self.graph = self.get_graph()

    def query_adjacent_stations(self, line_id, station_id, n):
        try:
            self.cursor.execute(sql.SQL("SELECT english_name from stations WHERE station_id = %s"), [station_id])
            english_name = self.cursor.fetchall()
            english_name = english_name[0][0]
            self.cursor.execute(
                sql.SQL("select nums from lines_detail where line_id = %s AND station_id = %s"),
                [line_id, station_id])
            nums = self.cursor.fetchall()
            nums = nums[0][0]
            self.cursor.execute(
                sql.SQL("SELECT distinct chinese_name, english_name FROM lines_detail "
                        "join stations on lines_detail.station_id = stations.station_id "
                        "WHERE line_id = %s AND (nums = %s - %s OR nums = %s + %s)"),
                [line_id, nums, n, nums, n]
            )
            results = self.cursor.fetchall()

            print("The stations that is the " + str(n) + "-th " + english_name + " ahead: " + results[0][1] + " (" +
                  results[0][0] + ")")
            print("The stations that is the " + str(n) + "-th " + english_name + " behind: " + results[1][1] + " (" +
                  results[1][0] + ")")

        except Exception as e:
            self.connection.rollback()
            print(f"Error adding line: {e}")

    def get_unfinished_passenger_rides(self):
        try:
            self.cursor.execute(
                sql.SQL("SELECT passenger_id, start_station, start_time FROM passenger_ride WHERE end_time IS NULL")
            )
            unfinished_passenger_rides = self.cursor.fetchall()

            return unfinished_passenger_rides
        except Exception as e:
            print(f"Error querying unfinished rides: {e}")
            return None, None

    def get_unfinished_card_rides(self):
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

    def get_graph(self):
        self.cursor.execute(sql.SQL(
            "SELECT line_id, station_id from lines_detail"
        ))
        results = self.cursor.fetchall()
        graph = defaultdict(list)
        for i in range(len(results) - 1):
            if results[i][0] == results[i + 1][0]:
                if not graph[results[i][1]].__contains__(results[i + 1][1]):
                    graph[results[i][1]].append(results[i + 1][1])
                if not graph[results[i + 1][1]].__contains__(results[i][1]):
                    graph[results[i + 1][1]].append(results[i][1])

        return graph

    def get_shortest_path(self, start_station, end_station):
        self.cursor.execute(sql.SQL(
            "SELECT station_id FROM stations WHERE english_name = %s"
        ), [start_station])
        start_station_id = self.cursor.fetchall()[0][0]
        self.cursor.execute(sql.SQL(
            "SELECT station_id FROM stations WHERE english_name = %s"
        ), [end_station])
        end_station_id = self.cursor.fetchall()[0][0]
        min_dist, shortest_path = self.dijkstra(start_station_id, end_station_id)
        return min_dist, shortest_path

    def dijkstra(self, start_station_id, end_station_id):
        shortest_path = []
        queue = [(0, start_station_id, shortest_path)]
        visited = set()
        min_dist = {start_station_id: 0}
        while queue:
            (cost, curr_station_id, path) = heapq.heappop(queue)
            if curr_station_id in visited:
                continue
            path = path + [curr_station_id]
            visited.add(curr_station_id)
            if curr_station_id == end_station_id:
                return cost, path
            for adjacent in self.graph[curr_station_id]:
                if adjacent in visited:
                    continue
                prev_cost = min_dist.get(adjacent, float('inf'))
                next_cost = cost + 1
                if next_cost < prev_cost:
                    min_dist[adjacent] = next_cost
                    heapq.heappush(queue, (next_cost, adjacent, path))
        if not shortest_path:
            return float('inf'), []
        else:
            return min_dist[start_station_id], shortest_path
