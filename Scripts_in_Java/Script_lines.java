import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.google.gson.stream.JsonWriter;

import java.io.*;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class Script_lines {

    public static void preprocessJson(String inputJsonFile, String outputJsonFile) {
        try (Reader reader = new FileReader(inputJsonFile)) {
            Type type = new TypeToken<Map<String, Map<String, Object>>>(){}.getType();
            Map<String, Map<String, Object>> originalData = new Gson().fromJson(reader, type);
            List<Map<String, Object>> transformedData = new ArrayList<>();

            originalData.forEach((lineName, details) -> {
                details.put("Chinese_name", lineName);
                transformedData.add(details);
            });

            try (Writer writer = new FileWriter(outputJsonFile);
                 JsonWriter jsonWriter = new JsonWriter(writer)) {
                jsonWriter.setIndent("    ");
                new Gson().toJson(transformedData, List.class, jsonWriter);
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void generateSql(String inputJsonFile, String outputSqlFile) {
        String createTable = """
            create table if not exists lines
            (
                line_id serial primary key,
                Chinese_name varchar(50) not null unique,
                start_time varchar(50) not null,
                end_time varchar(50) not null,
                mileage numeric(10,2) not null,
                color varchar(20) not null,
                first_opening varchar(50) not null,
                intro varchar(5000) not null,
                url varchar(100) not null
            );
            """;

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(outputSqlFile));
             Reader reader = new FileReader(inputJsonFile)) {
            writer.write(createTable + "\n");
            Type listType = new TypeToken<List<Map<String, Object>>>(){}.getType();
            List<Map<String, Object>> data = new Gson().fromJson(reader, listType);

            data.forEach(record -> {
                try {
                    String Chinese_name = ((String) record.get("Chinese_name")).replace("'", "''");
                    String start_time = ((String) record.get("start_time")).replace("'", "''");
                    String end_time = ((String) record.get("end_time")).replace("'", "''");
                    String temp = (String) record.get("mileage");
                    double mileage = Double.parseDouble(temp);
                    String color = ((String) record.get("color")).replace("'", "''");
                    String first_opening = ((String) record.get("first_opening")).replace("'", "''");
                    String intro = ((String) record.get("intro")).replace("'", "''");
                    String url = ((String) record.get("url")).replace("'", "''");

                    String insertSql = String.format("INSERT INTO lines (Chinese_name, start_time, end_time, mileage, color, first_opening, intro, url) VALUES ('%s', '%s', '%s', %.2f, '%s', '%s', '%s', '%s');\n",
                            Chinese_name, start_time, end_time, mileage, color, first_opening, intro, url);
                    writer.write(insertSql);
                } catch (IOException e) {
                    System.out.println("Error reading or writing JSON file: " + e.getMessage());
                }
            });
        } catch (IOException e) {
            System.out.println("Error reading or writing JSON file: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        String jsonInputPath = "C:\\Users\\Eric\\IdeaProjects\\CS307\\Project1\\resource\\lines.json";
        String jsonOutputPath = "C:\\Users\\Eric\\IdeaProjects\\CS307\\Project1\\out\\lines_adjusted.json";
        String sqlOutputPath = "C:\\Users\\Eric\\IdeaProjects\\CS307\\Project1\\out\\lines.sql";

        preprocessJson(jsonInputPath, jsonOutputPath);
        generateSql(jsonOutputPath, sqlOutputPath);
    }
}
