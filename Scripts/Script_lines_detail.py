import json

# Table Building Statement
create_table = """
    create table if not exists lines_detail
    (
        line_id     int not null,
        station_id  int not null,
        foreign key (line_id) references lines (line_id),
        foreign key (station_id) references stations (station_id),
        nums        int not null
    );
    """

# Information of Lines Stored on `Data`
try:
    with open('../out/lines_adjusted.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
except Exception as e:
    print(f"Error reading or loading lines_adjusted: {e}")
    exit(1)

# Build a Dictionary that Maps from `English_name` to `station_id`
try:
    with open('../out/stations_adjusted.json', 'r', encoding='utf-8') as file:
        stations_data = json.load(file)
        i = 0
        stations_dict = dict()
        for station in stations_data:
            i += 1
            stations_dict[station['English_name']] = i
except Exception as e:
    print(f"Error reading or loading lines_adjusted: {e}")
    exit(1)

try:
    with open('../out/lines_detail.sql', 'w', encoding='utf-8') as file:
        file.write(create_table + "\n")
        i = 0
        for lines in data:
            i += 1
            stations = lines['stations']
            j = 0
            for station in stations:
                j += 1
                station_id = stations_dict[station]
                insert_sql = f"INSERT INTO lines_detail (line_id, station_id, nums) VALUES ({i}, {station_id}, {j});\n"
                file.write(insert_sql)

except Exception as e:
    print(f"Error writing or saving line_detail: {e}")
