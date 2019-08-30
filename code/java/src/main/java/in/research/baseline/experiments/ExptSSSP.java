package in.research.baseline.experiments;

import in.research.baseline.queries.GetVertices;
import in.research.baseline.queries.tSSSP;
import in.research.graph.connectors.Graph;
import in.research.graph.connectors.TinkerGraphFactory;
import in.research.utils.Log;

import java.util.List;

public class ExptSSSP {

    public static void main(String Args[]) throws Exception {

        Log logger = new Log();

        TinkerGraphFactory tg = new TinkerGraphFactory();
        Graph g = tg.connectInstance("localhost", 8182);

        GetVertices getVertices = new GetVertices(g);

        List vertices = getVertices.runGetVertices(100);

        tSSSP sssp = new tSSSP(g);

        sssp.runSSSP(vertices, -1);

        logger.log("INFO", "Completed");

        System.exit(0);
    }

}
