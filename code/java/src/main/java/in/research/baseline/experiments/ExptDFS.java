package in.research.baseline.experiments;

import in.research.baseline.queries.tDFS;
import in.research.graph.connectors.Graph;
import in.research.graph.connectors.TinkerGraphFactory;
import in.research.utils.Log;
import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.GraphTraversalSource;

import java.util.List;

public class ExptDFS {

    public static void main(String Args[]) throws Exception {

        Log logger = new Log();

        TinkerGraphFactory tg = new TinkerGraphFactory();
        Graph graph = tg.connectInstance("localhost", 8182);

//        GraphTraversalSource g = (GraphTraversalSource) graph.getGraph();
//
//        logger.log("INFO", g.V(9509164L).outE().inV().toList());

        tDFS dfs = new tDFS(graph);

        List result = dfs.runDFS(9509164L, 1);

        logger.log("INFO", result);

        System.exit(0);
    }
}
