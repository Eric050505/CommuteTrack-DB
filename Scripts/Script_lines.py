import json


def preprocess_json(input_json_file, output_json_file):
    try:
        with open(input_json_file, 'r', encoding='utf-8') as file:
            original_data = json.load(file)
    except Exception as e:
        print(f"Error reading or loading the JSON file: {e}")
        exit(1)

    transformed_data = []
    for line_name, details in original_data.items():
        new_entry = {
            "Chinese_name": line_name
        }
        new_entry.update(details)
        transformed_data.append(new_entry)

    try:
        with open(output_json_file, 'w', encoding='utf-8') as file:
            json.dump(transformed_data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error writing or saving the transformed JSON file: {e}")
        exit(1)


def generate_sql(input_json_file, output_sql_file):
    create_table = """
    create table if not exists lines
    (
        line_id serial  primary key,
        Chinese_name varchar(50) not null unique,
        start_time varchar(50) not null,
        end_time varchar(50) not null,
        mileage numeric(10,2) not null,
        color varchar(20) not null,
        first_opening varchar(50) not null,
        intro varchar(5000) not null,
        url varchar(100) not null
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
                chinese_name = record["Chinese_name"].replace("'", "''")
                start_time = record["start_time"].replace("'", "''")
                end_time = record["end_time"].replace("'", "''")
                mileage = record["mileage"]
                color = record["color"].replace("'", "''")
                first_opening = record["first_opening"].replace("'", "''")
                intro = record["intro"].replace("'", "''")
                url = record["url"].replace("'", "''")

                insert_sql = (f"INSERT INTO lines "
                              f"(Chinese_name, start_time, end_time, mileage, color, first_opening, intro,  url) "
                              f"VALUES ('{chinese_name}', '{start_time}', '{end_time}',  {mileage}, '{color}',"
                              f" '{first_opening}', '{intro}', '{url}');\n")
                file.write(insert_sql)
    except Exception as e:
        print(f"Error writing or saving the transformed JSON file: {e}")


json_input_path = '../resource/lines.json'  # original JSON file path
json_output_path = '../out/lines_adjusted.json'  # adjusted JSON file path
sql_output_path = '../out/lines.sql'  # SQL file path

preprocess_json(json_input_path, json_output_path)
generate_sql(json_output_path, sql_output_path)
