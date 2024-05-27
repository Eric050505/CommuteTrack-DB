import org.json.JSONArray;
import org.json.JSONObject;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.sql.Timestamp;
import java.text.SimpleDateFormat;

public class Script_cards {

    public static void main(String[] args) {
        String createTableSql = """
                create table if not exists cards
                (
                    card_id serial unique,
                    code int not null
                        primary key,
                    money float not null,
                    create_time timestamp not null
                );
                """;

        String jsonFilePath = "C:\\Users\\Eric\\IdeaProjects\\CS307\\Project1\\resource\\cards.json";
        String sqlFilePath = "C:\\Users\\Eric\\IdeaProjects\\CS307\\Project1\\out\\cards.sql";

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
                    int code = record.getInt("code");
                    double money = record.getDouble("money");
                    String createTimeStr = record.getString("create_time");
                    Timestamp createTime = Timestamp.valueOf(createTimeStr);

                    String insertSql = String.format("INSERT INTO cards (code, money, create_time) VALUES (%d, %.2f, '%s');\n",
                            code, money, new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(createTime));                    writer.write(insertSql);
                }
            }
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
