import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.io.*;
import java.lang.reflect.Type;
import java.util.List;
import java.util.Map;
import java.util.HashMap;

public class Script_out_info {

    public static void main(String[] args) {
        String createTableSql = """
            create table if not exists out_info
            (
                station_id int not null,
                foreign key (station_id) references stations (station_id),
                exit_name varchar(200),
                exit_info varchar(2000)
            );
            """;

        List<Map<String, Object>> stationData = readJson("C:\\Users\\Eric\\IdeaProjects\\CS307\\Project1\\out\\stations_adjusted.json");
        Map<String, Integer> stationIds = new HashMap<>();
        for (int i = 0; i < stationData.size(); i++) {
            stationIds.put((String) stationData.get(i).get("English_name"), i + 1);
        }

        writeSql(stationData, stationIds, createTableSql, "C:\\Users\\Eric\\IdeaProjects\\CS307\\Project1\\out\\out_info.sql");
    }

    private static List<Map<String, Object>> readJson(String filePath) {
        try (Reader reader = new FileReader(filePath)) {
            Type listType = new TypeToken<List<Map<String, Object>>>(){}.getType();
            return new Gson().fromJson(reader, listType);
        } catch (IOException e) {
            System.err.println("Error reading JSON file: " + filePath);
            e.printStackTrace();
            return null;
        }
    }

    private static void writeSql(List<Map<String, Object>> data, Map<String, Integer> stationIds, String createTableSql, String outputPath) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(outputPath))) {
            writer.write(createTableSql + "\n");

            for (Map<String, Object> record : data) {
                int stationId = stationIds.get(record.get("English_name"));
                List<Map<String, String>> outInfos = (List<Map<String, String>>) record.get("out_info");
                for (Map<String, String> outInfo : outInfos) {
                    String exitName = outInfo.get("outt").replace("'", "''");
                    String exitInfo = outInfo.get("textt").replace("'", "''");
                    String insertSql = String.format("INSERT INTO out_info (station_id, exit_name, exit_info) VALUES (%d, '%s', '%s');\n",
                            stationId, exitName, exitInfo);
                    writer.write(insertSql);
                }
            }
        } catch (IOException e) {
            System.err.println("Error writing SQL file: " + outputPath);
            e.printStackTrace();
        }
    }
}
