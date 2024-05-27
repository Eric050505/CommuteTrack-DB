import org.json.JSONArray;
import org.json.JSONObject;

import java.io.*;
import java.nio.charset.StandardCharsets;

public class Script_passenger {

    public static void main(String[] args) {
        String createTableSql = """
                create table if not exists passenger
                (
                    passenger_id serial unique,
                    id_number varchar(50) not null primary key,
                    name varchar(50) not null,0
                    phone_number varchar(50) not null,
                    gender varchar(5) not null,
                    district varchar(50) not null
                );
                """;

        String jsonFilePath = "C:\\Users\\Eric\\IdeaProjects\\CS307\\Project1\\resource\\passenger.json";
        String sqlFilePath = "C:\\Users\\Eric\\IdeaProjects\\CS307\\Project1\\out\\passenger.sql";

        try (BufferedReader reader = new BufferedReader(new FileReader(jsonFilePath, StandardCharsets.UTF_8))) {
            StringBuilder contentBuilder = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                contentBuilder.append(line);
            }
            String jsonData = contentBuilder.toString();
            JSONArray data = new JSONArray(jsonData);

            try (BufferedWriter writer = new BufferedWriter(new FileWriter(sqlFilePath, StandardCharsets.UTF_8))) {
                writer.write(createTableSql);
                for (int i = 0; i < data.length(); i++) {
                    JSONObject record = data.getJSONObject(i);
                    String idNumber = record.getString("id_number").replace("'", "''");
                    String name = record.getString("name").replace("'", "''");
                    String phoneNumber = record.getString("phone_number").replace("'", "''");
                    String gender = record.getString("gender").replace("'", "''");
                    String district = record.getString("district").replace("'", "''");

                    String insertSql = String.format("INSERT INTO passenger (id_number, name, phone_number, gender, district) VALUES ('%s', '%s', '%s', '%s', '%s');\n",
                            idNumber, name, phoneNumber, gender, district);
                    writer.write(insertSql);
                }
            }
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
