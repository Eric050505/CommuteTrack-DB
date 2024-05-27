import json

create_table = """
    create table if not exists bus_info
    (
        station_id int not null,
        foreign key (station_id) references stations (station_id),
        exit_name varchar(200) not null,
        bus_name varchar(80),
        bus_info varchar(2000)
       
    );
    """

try:
    with open('../out/stations_adjusted.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        i = 0
        stations_dict = dict()
        for station in data:
            i += 1
            stations_dict[station['English_name']] = i
except Exception as e:
    print(f"Error reading or loading lines_adjusted: {e}")
    exit(1)

try:
    with open('../out/bus_info.sql', 'w', encoding='utf-8') as file:
        file.write(create_table + "\n")
        i = 0
        for record in data:
            station_id = stations_dict[record['English_name']]
            for busInfo in record['bus_info']:
                exit_name = busInfo['chukou']
                for bufOutInfo in busInfo['busOutInfo']:
                    bus_name = bufOutInfo['busName']
                    bus_info = bufOutInfo['busInfo']
                    insert_sql = (f"INSERT INTO bus_info (station_id, exit_name, bus_name, bus_info) "
                                  f"VALUES ({station_id}, '{exit_name}', '{bus_name}', '{bus_info}');\n")
                    file.write(insert_sql)

except Exception as e:
    print(f"Error writing or saving line_detail: {e}")
