import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.io.*;
import java.lang.reflect.Type;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Script_bus_info {

    public static void main(String[] args) {
        String createTableSql = """
            create table if not exists bus_info
            (
                station_id int not null,
                foreign key (station_id) references stations (station_id),
                exit_name varchar(200) not null,
                bus_name varchar(80),
                bus_info varchar(2000)
            );
            """;

        List<Map<String, Object>> stationData = readJson("C:\\Users\\Eric\\IdeaProjects\\CS307\\Project1\\out\\stations_adjusted.json");
        Map<String, Integer> stationIds = new HashMap<>();
        for (int i = 0; i < stationData.size(); i++) {
            stationIds.put((String) stationData.get(i).get("English_name"), i + 1);
        }

        writeSql(stationData, stationIds, createTableSql, "C:\\Users\\Eric\\IdeaProjects\\CS307\\Project1\\out\\bus_info.sql");
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
                List<Map<String, Object>> busInfos = (List<Map<String, Object>>) record.get("bus_info");
                for (Map<String, Object> busInfo : busInfos) {
                    String exitName = ((String) busInfo.get("chukou")).replace("'", "''");
                    List<Map<String, String>> busOutInfos = (List<Map<String, String>>) busInfo.get("busOutInfo");
                    for (Map<String, String> busOutInfo : busOutInfos) {
                        String busName = busOutInfo.get("busName").replace("'", "''");
                        String busDetails = busOutInfo.get("busInfo").replace("'", "''");
                        String insertSql = String.format("INSERT INTO bus_info (station_id, exit_name, bus_name, bus_info) VALUES (%d, '%s', '%s', '%s');\n",
                                stationId, exitName, busName, busDetails);
                        writer.write(insertSql);
                    }
                }
            }
        } catch (IOException e) {
            System.err.println("Error writing SQL file: " + outputPath);
            e.printStackTrace();
        }
    }
}
