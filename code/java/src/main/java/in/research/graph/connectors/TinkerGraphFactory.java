package in.research.graph.connectors;

import org.apache.tinkerpop.gremlin.driver.remote.DriverRemoteConnection;
import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.GraphTraversalSource;

import java.util.Map;

import static org.apache.tinkerpop.gremlin.process.traversal.AnonymousTraversalSource.traversal;

public class TinkerGraphFactory implements GraphFactory {

    public Graph connectInstance(String server, Integer port) {
        GraphTraversalSource g = traversal().withRemote(DriverRemoteConnection.using(server, port, "g"));
        return new Graph<>(g);
    }

    public Graph connectInstance(String server, Integer port, Map<String, String> params) {
        GraphTraversalSource g = traversal().withRemote(DriverRemoteConnection.using(server, port, "g"));
        return new Graph<>(g);
    }

}
