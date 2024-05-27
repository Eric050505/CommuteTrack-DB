import org.json.JSONArray;
import org.json.JSONObject;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.Iterator;

public class error_Script_lines {

    public static void preprocessJson(String inputJsonFile, String outputJsonFile) {
        try (BufferedReader reader = new BufferedReader(new FileReader(inputJsonFile, StandardCharsets.UTF_8))) {
            StringBuilder contentBuilder = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                contentBuilder.append(line);
            }
            String originalData = contentBuilder.toString();
            JSONObject jsonObject = new JSONObject(originalData);

            JSONArray transformedData = new JSONArray();
            Iterator<String> keys = jsonObject.keys();
            while (keys.hasNext()) {
                String lineName = keys.next();
                JSONObject details = jsonObject.getJSONObject(lineName);
                JSONObject newEntry = new JSONObject();
                newEntry.put("Chinese_name", lineName);
                for (String key : details.keySet()) {
                    newEntry.put(key, details.get(key));
                }
                transformedData.put(newEntry);
            }

            try (BufferedWriter writer = new BufferedWriter(new FileWriter(outputJsonFile, StandardCharsets.UTF_8))) {
                writer.write(transformedData.toString(4));
            }
        } catch (Exception e) {
            System.out.println("Error reading or loading the JSON file: " + e.getMessage());
            System.exit(1);
        }
    }

    public static void generateSql(String inputJsonFile, String outputSqlFile) {
        String createTable = """
                create table if not exists lines
                (
                    line_id serial  primary key,
                    Chinese_name varchar(50) not null unique,
                    start_time varchar(50) not null,
                    end_time varchar(50) not null,
                    intro varchar(5000) not null,
                    mileage numeric(10,2) not null,
                    color varchar(20) not null,
                    first_opening varchar(50) not null,
                    url varchar(100) not null
                );
                """;

        try (BufferedReader reader = new BufferedReader(new FileReader(inputJsonFile, StandardCharsets.UTF_8))) {
            StringBuilder contentBuilder = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                contentBuilder.append(line);
            }
            JSONArray data = new JSONArray(contentBuilder.toString());

            try (BufferedWriter writer = new BufferedWriter(new FileWriter(outputSqlFile, StandardCharsets.UTF_8))) {
                writer.write(createTable);
                for (int i = 0; i < data.length(); i++) {
                    JSONObject record = data.getJSONObject(i);
                    String chineseName = record.getString("Chinese_name").replace("'", "''");
                    String startTime = record.getString("start_time").replace("'", "''");
                    String endTime = record.getString("end_time").replace("'", "''");
                    String intro = record.getString("intro").replace("'", "''");
                    double mileage = record.getDouble("mileage");
                    String color = record.getString("color").replace("'", "''");
                    String firstOpening = record.getString("first_opening").replace("'", "''");
                    String url = record.getString("url").replace("'", "''");

                    String insertSql = String.format("INSERT INTO lines (Chinese_name, start_time, end_time, intro, mileage, color, first_opening, url) VALUES ('%s', '%s', '%s', '%s', %.2f, '%s', '%s', '%s');\n", chineseName, startTime, endTime, intro, mileage, color, firstOpening, url);
                    writer.write(insertSql);
                }
            }
        } catch (Exception e) {
            System.out.println("Error writing or saving the transformed JSON file: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        String jsonInputPath = "C:\\Users\\Eric\\IdeaProjects\\CS307\\Project1\\resource\\lines.json"; // original JSON file path
        String jsonOutputPath = "C:\\Users\\Eric\\IdeaProjects\\CS307\\Project1\\out\\error_lines_adjusted.json"; // adjusted JSON file path
        String sqlOutputPath = "C:\\Users\\Eric\\IdeaProjects\\CS307\\Project1\\out\\error_lines.sql"; // SQL file path

        preprocessJson(jsonInputPath, jsonOutputPath);
        generateSql(jsonOutputPath, sqlOutputPath);
    }
}
