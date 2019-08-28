package in.research.graph.connectors;

import java.util.Map;

public interface GraphFactory {

    Graph connectInstance(String server, Integer port);

    Graph connectInstance(String server, Integer port, Map<String, String> params);

}
