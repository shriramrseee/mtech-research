package in.research.baseline.queries;

import in.research.graph.connectors.Graph;
import in.research.utils.Log;
import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.GraphTraversal;
import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.GraphTraversalSource;
import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.__;
import org.apache.tinkerpop.gremlin.structure.Vertex;
import org.apache.tinkerpop.gremlin.util.function.Lambda;

import java.io.IOException;
import java.util.List;

import static org.apache.tinkerpop.gremlin.process.traversal.P.without;
import static org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.__.outE;

public class tSSSP {
    private Graph graph;
    private Log logger;

    public tSSSP(Graph g) throws IOException {
        graph = g;
        logger = new Log();
    }

    public List runSSSP(Long SourceID, Integer Steps) throws Exception {


        GraphTraversalSource g = (GraphTraversalSource) graph.getGraph();

        logger.log("INFO", "Start tSSSP for Vertex,Steps: " + SourceID.toString() + "," + Steps.toString());

        GraphTraversal<Vertex, Vertex> t = g.withSack(Lambda.supplier("[:]"))
                .V(SourceID)
                .sack(Lambda.biFunction("m, v -> m['arrival'] = [:]; m"))
                .sack(Lambda.biFunction("m, v -> m['parent'] = [:]; m"))
                .sack(Lambda.biFunction("m, v -> m['pre_arrival'] = [:]; m"))
                .sack(Lambda.biFunction("m, v -> m['pre_parent'] = [:]; m"))
                .sack(Lambda.biFunction("m, v -> m['edge'] = [:]; m"))
                .sack(Lambda.biFunction("m, v -> m['arrival'][v.id()] = v.value('start_time'); m"))
                .sack(Lambda.biFunction("m, v -> m['parent'][v.id()] = -1; m"))
                .repeat(
                        outE()
                                .sack(Lambda.biFunction("m, e -> m['edge'][e.id()] =  m['arrival'][e.outVertex().id()] > e.value('start_time') ? m['arrival'][e.outVertex().id()] : e.value('start_time') ; m"))
                                .filter(__.as("b")
                                        .sack().as("c")
                                        .select("b", "c")
                                        .map(Lambda.function("it -> it.path().get('c')['arrival'][it.path().get('b').outVertex().id()] < it.path().get('b').value('end_time') &&" +
                                                "(!it.path().get('c')['arrival'].containsKey(it.path().get('b').outVertex().id()) ||" +
                                                " it.path().get('c')['arrival'][it.path().get('b').outVertex().id()] > " +
                                                "it.path().get('c')['edge'][it.path().get('b').id()])"))
                                )
                                .sack(Lambda.biFunction("m, e -> m['pre_arrival'][e.inVertex().id()] = m['pre_arrival'].containsKey(e.inVertex().id())?" +
                                        " (m['edge'][e.id()] < m['pre_arrival'][e.inVertex().id()] ? m['edge'][e.id()] :  m['pre_arrival'][e.inVertex().id()]) : m['edge'][e.id()]; m"))
                                .sack(Lambda.biFunction("m, e -> m['pre_parent'][e.inVertex().id()] = m['edge'][e.id()] == m['pre_arrival'][e.inVertex().id()] ? e.outVertex().id():m['pre_parent'][e.inVertex().id()]; m"))
                                .inV()
                                .dedup()
                                .sack(Lambda.biFunction("m, v -> m['arrival'][v.id()] =  m['pre_arrival'][v.id()]; m"))
                                .sack(Lambda.biFunction("m, v -> m['parent'][v.id()] =  m['pre_parent'][v.id()]; m"))
                );

        List ssspList;

        if (Steps == -1) {
            ssspList = t.tail(1)
                    .sack()
                    .map(Lambda.function("it -> [it.sack()['arrival'], it.sack()['parent']]"))
                    .toList();
        } else {
            ssspList = t.times(Steps)
                    .tail(1)
                    .sack()
                    .map(Lambda.function("it -> [it.sack()['arrival'], it.sack()['parent']]"))
                    .toList();
        }

        logger.log("INFO", "Finish tSSSP for Vertex,Steps: " + SourceID.toString() + "," + Steps.toString());

        g.close();

        return ssspList;

    }
}
