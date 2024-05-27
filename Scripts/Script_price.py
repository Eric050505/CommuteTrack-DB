import csv
import pandas as pd
import psycopg2

input_excel_path = r"E:\Users\Eric\PycharmProjects\CS307\Project\resource\Price.xlsx"
output_csv_temp_path = "../out/price_adjusted.csv"
output_csv_path = "../out/price.csv"
output_sql_path = "../out/price.sql"

df = pd.read_excel(input_excel_path)
df.to_csv(output_csv_temp_path, index=False)


station_map = {}
connect = psycopg2.connect(host='localhost', user='checker', password='123456', database='cs307', port=5432)
cursor = connect.cursor()
cursor.execute("SET search_path TO project")
sql = ("create table if not exists price "
       "( start_station_id int not null, foreign key (start_station_id) references stations (station_id), "
       "end_station_id int not null, foreign key (end_station_id) references stations (station_id), price int );")
cursor.execute(sql)
sql = "SELECT * FROM stations"
cursor.execute(sql)
stations = cursor.fetchall()
for station in stations:
    station_map[station[1]] = station[0]
connect.commit()
connect.close()
station_map['深圳北站'] = 95

price_data = [("start_station_id", "end_station_id", "price")]
df = pd.read_csv(output_csv_temp_path)
for i in range(2, 375):
    lines1 = station_map[df.iloc[i, 2]]
    for j in range(3, 376):
        lines2 = station_map[df.iloc[1, j]]
        price = df.iloc[i, j]
        price_data.append([lines1, lines2, price])

with open(output_csv_path, "w", encoding='utf-8', newline="") as f:
    writer = csv.writer(f)
    writer.writerows(price_data)
