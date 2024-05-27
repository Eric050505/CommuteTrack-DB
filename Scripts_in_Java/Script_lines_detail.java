import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.io.*;
import java.lang.reflect.Type;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Script_lines_detail {

    public static void main(String[] args) {
        String createTableSql = """
            create table if not exists lines_detail
            (
                line_id     int not null,
                station_id  int not null,
                foreign key (line_id) references lines (line_id),
                foreign key (station_id) references stations (station_id)
            );
            """;

        List<Map<String, Object>> linesData = readJson("C:\\Users\\Eric\\IdeaProjects\\CS307\\Project1\\out\\lines_adjusted.json");
        List<Map<String, Object>> stationsData = readJson("C:\\Users\\Eric\\IdeaProjects\\CS307\\Project1\\out\\stations_adjusted.json");

        Map<String, Integer> stationsDict = new HashMap<>();
        for (int i = 0; i < stationsData.size(); i++) {
            String englishName = (String) stationsData.get(i).get("English_name");
            stationsDict.put(englishName, i + 1);  // Assuming station IDs start at 1
        }

        writeSql(linesData, stationsDict, createTableSql, "C:\\Users\\Eric\\IdeaProjects\\CS307\\Project1\\out\\lines_detail.sql");
    }

    private static List<Map<String, Object>> readJson(String filePath) {
        try (Reader reader = new FileReader(filePath)) {
            Type type = new TypeToken<List<Map<String, Object>>>(){}.getType();
            return new Gson().fromJson(reader, type);
        } catch (IOException e) {
            System.err.println("Error reading or loading file: " + filePath);
            System.err.println(e.getMessage());
            return null;
        }
    }

    private static void writeSql(List<Map<String, Object>> linesData, Map<String, Integer> stationsDict, String createTableSql, String outputPath) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(outputPath))) {
            writer.write(createTableSql + "\n");

            int lineId = 1;
            for (Map<String, Object> line : linesData) {
                List<String> stations = (List<String>) line.get("stations");
                for (String station : stations) {
                    Integer stationId = stationsDict.get(station);
                    if (stationId != null) {
                        String insertSql = String.format("INSERT INTO lines_detail (line_id, station_id) VALUES (%d, %d);\n", lineId, stationId);
                        writer.write(insertSql);
                    }
                }
                lineId++;
            }
        } catch (IOException e) {
            System.err.println("Error writing to SQL file: " + outputPath);
            System.err.println(e.getMessage());
        }
    }
}
