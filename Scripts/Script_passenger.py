import json

create_table = """
create table if not exists passenger
(
    passenger_id serial unique,
    id_number  varchar(50) not null primary key,
    name    varchar(50) not null,
    phone_number  varchar(50) not null,
    gender  varchar(5) not null,
    district   varchar(50) not null
);
"""

try:
    with open('../resource/passenger.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
except Exception as e:
    print(f"Error reading or loading the JSON file: {e}")
    exit(1)

try:
    with open('../out/passenger.sql', 'w', encoding='utf-8') as file:
        file.write(create_table + "\n")
        for record in data:
            id_number = record['id_number'].replace("'", "''")
            name = record['name'].replace("'", "''")
            phone_number = record['phone_number'].replace("'", "''")
            gender = record['gender'].replace("'", "''")
            district = record['district'].replace("'", "''")

            file.write(f"INSERT INTO passenger (id_number, name, phone_number, gender, district) "
                       f"VALUES ('{id_number}', '{name}', '{phone_number}', '{gender}', '{district}');\n")
except Exception as e:
    print(f"Error writing to the SQL file: {e}")
