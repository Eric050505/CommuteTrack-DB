import json


def preprocess_json(input_json_file, output_json_file):
    try:
        with open(input_json_file, 'r', encoding='utf-8') as file:
            original_data = json.load(file)
    except Exception as e:
        print(f"Error reading or loading the JSON file: {e}")
        exit(1)

    transformed_data = []
    for English_name, details in original_data.items():
        new_entry = {
            "English_name": English_name
        }
        new_entry.update(details)
        transformed_data.append(new_entry)

    try:
        with open(output_json_file, 'w', encoding='utf-8') as file:
            json.dump(transformed_data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error writing output file: {e}")
        exit(1)


def generate_sql(input_json_file, output_sql_file):
    create_table = """
        create table if not exists stations
        (
            station_id serial  primary key,
            Chinese_name varchar(50) not null unique,
            English_name varchar(50) not null unique,
            district varchar(50) not null,
            intro varchar(5000) not null
        );
        """

    try:
        with open(input_json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except Exception as e:
        print(f"Error reading or loading the JSON file: {e}")
        exit(1)

    try:
        with open(output_sql_file, 'w', encoding='utf-8') as file:
            file.write(create_table + "\n")
            for record in data:
                english_name = record['English_name'].replace("'", "''").replace("\n", "")
                chinese_name = record['chinese_name'].replace("'", "''")
                intro = record['intro'].replace("'", "''")
                district = record['district']

                insert_sql = (f"INSERT INTO stations (Chinese_name, English_name, district, intro) "
                              f"VALUES ('{chinese_name}', '{english_name}', '{district}', '{intro}');\n")
                file.write(insert_sql)
    except Exception as e:
        print(f"Error with reading the JSON file: {e}")


json_input_path = '../resource/stations.json'  # original JSON file path
json_output_path = '../out/stations_adjusted.json'  # adjusted JSON file path
sql_output_path = '../out/stations.sql'  # SQL file path

preprocess_json(json_input_path, json_output_path)
generate_sql(json_output_path, sql_output_path)
