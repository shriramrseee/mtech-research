package in.research.baseline.experiments;

import in.research.baseline.queries.tBFS;
import in.research.graph.connectors.Graph;
import in.research.graph.connectors.TinkerGraphFactory;
import in.research.utils.Log;

import java.util.List;

public class ExptBFS {

    public static void main(String Args[]) throws Exception {

        Log logger = new Log();

        TinkerGraphFactory tg = new TinkerGraphFactory();
        Graph g = tg.connectInstance("localhost", 8182);

        tBFS bfs = new tBFS(g);

        List result = bfs.runBFS(9306117L, 1);

        logger.log("INFO", result);

        System.exit(0);
    }

}
