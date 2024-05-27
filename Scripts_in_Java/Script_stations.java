import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.google.gson.stream.JsonWriter;

import java.io.*;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class Script_stations {

    public static void preprocessJson(String inputJsonFile, String outputJsonFile) {
        try (Reader reader = new FileReader(inputJsonFile)) {
            Type type = new TypeToken<Map<String, Map<String, Object>>>(){}.getType();
            Map<String, Map<String, Object>> originalData = new Gson().fromJson(reader, type);
            List<Map<String, Object>> transformedData = new ArrayList<>();

            originalData.forEach((englishName, details) -> {
                details.put("English_name", englishName);
                transformedData.add(details);
            });

            try (Writer writer = new FileWriter(outputJsonFile);
                 JsonWriter jsonWriter = new JsonWriter(writer)) {
                jsonWriter.setIndent("    ");
                new Gson().toJson(transformedData, List.class, jsonWriter);
            }

        } catch (IOException e) {
            System.out.println("Error reading or writing JSON file: " + e.getMessage());
        }
    }

    public static void generateSql(String inputJsonFile, String outputSqlFile) {
        String createTable = """
            create table if not exists stations
            (
                station_id serial primary key,
                Chinese_name varchar(50) not null unique,
                English_name varchar(50) not null unique,
                district varchar(50) not null,
                intro varchar(5000) not null
            );
            """;

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(outputSqlFile));
             Reader reader = new FileReader(inputJsonFile)) {
            writer.write(createTable + "\n");
            Type listType = new TypeToken<List<Map<String, Object>>>(){}.getType();
            List<Map<String, Object>> data = new Gson().fromJson(reader, listType);

            data.forEach(record -> {
                try {
                    String English_name = ((String) record.get("English_name")).replace("'", "''").replace("\n", "");
                    String Chinese_name = ((String) record.get("chinese_name")).replace("'", "''");
                    String intro = ((String) record.get("intro")).replace("'", "''");
                    String district = (String) record.get("district");

                    String insertSql = String.format("INSERT INTO stations (Chinese_name, English_name, district, intro) VALUES ('%s', '%s', '%s', '%s');\n",
                            Chinese_name, English_name, district, intro);
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
        String jsonInputPath = "C:\\Users\\Eric\\IdeaProjects\\CS307\\Project1\\resource\\stations.json";
        String jsonOutputPath = "C:\\Users\\Eric\\IdeaProjects\\CS307\\Project1\\out\\stations_adjusted.json";
        String sqlOutputPath = "C:\\Users\\Eric\\IdeaProjects\\CS307\\Project1\\out\\stations.sql";

        preprocessJson(jsonInputPath, jsonOutputPath);
        generateSql(jsonOutputPath, sqlOutputPath);
    }
}
