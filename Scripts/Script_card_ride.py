import json
import time

start_time = time.time()

create_table = """
create table if not exists card_ride
(
    card_ride_id serial unique,
    primary key (card_code, start_time),
    card_code    int not null,
    foreign key (card_code) references cards (code),
    start_station    varchar(50) not null,
    foreign key (start_station) references stations(english_name),
    end_station    varchar(50) not null,
    foreign key (end_station) references stations(english_name),
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
    with open('../out/card_ride.sql', 'w', encoding='utf-8') as file:
        file.write(create_table + "\n")
        for record in data:
            start_station = record['start_station'].replace('\'', '\'\'').replace('\n', '')
            end_station = record['end_station'].replace('\'', '\'\'').replace('\n', '')
            id = record['user'].replace('\'', '\'\'')
            if len(id) == 9:
                file.write(f"INSERT INTO card_ride (card_code, start_station, end_station, price, start_time, end_time) VALUES ({id}, '{start_station}', '{end_station}', {record['price']}, '{record['start_time']}', '{record['end_time']}');\n")
except Exception as e:
    print(f"Error writing to the SQL file: {e}")


end_time = time.time()
print(f"Time cost: {end_time - start_time} seconds")
