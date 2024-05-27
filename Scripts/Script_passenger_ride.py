import json

# SQL statement to create a table
create_table = """
create table if not exists passenger_ride
(
    passenger_ride_id serial,
    primary key (passenger_id, start_time),
    passenger_id    varchar(50) not null,
    foreign key (passenger_id) references passenger (id_number),
    start_station    varchar(50) not null,
    foreign key (start_station) references stations (english_name),
    end_station    varchar(50) not null,
    foreign key (end_station) references stations (english_name),
    price   int not null,
    start_time  timestamp not null,
    end_time  timestamp not null
);
"""

try:
    with open('../resource/ride.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
except Exception as e:
    print(f"Error reading or loading the JSON file: {e}")
    exit(1)

try:
    with open('../out/passenger_ride.sql', 'w', encoding='utf-8') as file:
        file.write(create_table + "\n")
        for record in data:
            start_station = record['start_station'].replace('\'', '\'\'').replace('\n', '')
            end_station = record['end_station'].replace('\'', '\'\'').replace('\n', '')
            id = record['user'].replace('\'', '\'\'')
            if len(id) == 18:
                file.write(f"INSERT INTO passenger_ride "
                           f"(passenger_id, start_station, end_station, price, start_time, end_time) "
                           f"VALUES ('{id}', '{start_station}', '{end_station}', {record['price']}, "
                           f"'{record['start_time']}', '{record['end_time']}');\n")
except Exception as e:
    print(f"Error writing to the SQL file: {e}")
