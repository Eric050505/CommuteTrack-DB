import org.json.JSONArray;
import org.json.JSONObject;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.sql.Timestamp;
import java.text.SimpleDateFormat;

public class Script_card_ride {

    public static void main(String[] args) {
        String createTableSql = """
                create table if not exists card_ride
                (
                    card_ride_id serial unique,
                    primary key (card_code, start_time),
                    card_code    int not null,
                    foreign key (card_code) references cards (code),
                    start_station    varchar(50) not null,
                    foreign key (start_station) references stations(english_name),
                    end_station    varchar(50) not null,
                    foreign key (end_station) references stations(english_name),
                    price   int not null,
                    start_time  timestamp not null,
                    end_time  timestamp not null
                );
                """;

        String jsonFilePath = "C:\\Users\\Eric\\IdeaProjects\\CS307\\Project1\\resource\\ride.json";
        String sqlFilePath = "C:\\Users\\Eric\\IdeaProjects\\CS307\\Project1\\out\\card_ride.sql";

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
                    String startStation = record.getString("start_station").replace("'", "''").replace("\n", "");
                    String endStation = record.getString("end_station").replace("'", "''").replace("\n", "");
                    String id = record.getString("user").replace("'", "''");
                    if (id.length() != 9) continue;
                    int price = record.getInt("price");
                    String startTimeStr = record.getString("start_time");
                    String endTimeStr = record.getString("end_time");
                    Timestamp startTime = Timestamp.valueOf(startTimeStr);
                    Timestamp endTime = Timestamp.valueOf(endTimeStr);

                    String insertSql = String.format("INSERT INTO card_ride (card_code, start_station, end_station, price, start_time, end_time) VALUES (%d, '%s', '%s', %d, '%s', '%s');\n",
                            Integer.parseInt(id), startStation, endStation, price, new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(startTime), new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(endTime));
                    writer.write(insertSql);
                }
            }
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
