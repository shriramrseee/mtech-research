package in.research.baseline.queries;

import in.research.graph.connectors.Graph;
import in.research.utils.Log;
import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.GraphTraversalSource;

import java.io.IOException;
import java.util.List;

public class GetVertices {

    private Graph graph;
    private Log logger;

    public GetVertices(Graph g) throws IOException {
        graph = g;
        logger = new Log();
    }

    public List runGetVertices(int numVertices) throws Exception {

        GraphTraversalSource g = (GraphTraversalSource) graph.getGraph();

        return g.V().sample(numVertices).id().toList();

    }

}
