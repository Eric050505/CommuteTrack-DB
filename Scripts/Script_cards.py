import json

create_table = """create table if not exists cards
(
    card_id serial unique,
    code    int not null
        primary key,
    money   float not null,
    create_time  timestamp not null
);"""

try:
    with open('../resource/cards.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
except Exception as e:
    print(f"Error reading or loading cards: {e}")
    exit(1)

try:
    with open('../out/cards.sql', 'w', encoding='utf-8') as file:
        file.write(create_table + "\n")
        for record in data:
            file.write("INSERT INTO cards (code, money, create_time) VALUES (" + record['code'] + ", " + str(
                record['money']) + ", \'" + record['create_time'] + "\');\n")
except Exception as e:
    print(f"Error writing or saving cards: {e}")
