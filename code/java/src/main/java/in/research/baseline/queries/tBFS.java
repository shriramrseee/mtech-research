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

import static org.apache.tinkerpop.gremlin.process.traversal.P.*;
import static org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.__.*;

public class tBFS {

    private Graph graph;
    private Log logger;

    public tBFS(Graph g) throws IOException {
        graph = g;
        logger = new Log();
    }

    public void runBFS(List<Long> Source, Integer Steps) throws Exception {


        GraphTraversalSource g = (GraphTraversalSource) graph.getGraph();

        Long avgTime = 0L;
        Long start = 0L;
        Long end = 0L;

        for(Long SourceID : Source) {

            start = System.currentTimeMillis();

            GraphTraversal<Vertex, Vertex> t = g.withSack(Lambda.supplier("[:]"))
                    .V(SourceID)
                    .store("visitedSet")
                    .sack(Lambda.biFunction("m, v -> m['arrival'] = [:]; m"))
                    .sack(Lambda.biFunction("m, v -> m['parent'] = [:]; m"))
                    .sack(Lambda.biFunction("m, v -> m['pre_arrival'] = [:]; m"))
                    .sack(Lambda.biFunction("m, v -> m['pre_parent'] = [:]; m"))
                    .sack(Lambda.biFunction("m, v -> m['arrival'][v.id()] = v.value('start_time'); m"))
                    .sack(Lambda.biFunction("m, v -> m['parent'][v.id()] = -1; m"))
                    .repeat(
                            outE()
                                    .filter(__.as("b")
                                            .sack().as("c")
                                            .select("b", "c")
                                            .map(Lambda.function("it -> it.path().get('c')['arrival'][it.path().get('b').outVertex().id()] < it.path().get('b').value('end_time')"))
                                    )
                                    .sack(Lambda.biFunction("m, e -> m['pre_arrival'][e.inVertex().id()] = m['arrival'][e.outVertex().id()] > e.value('start_time') ? m['arrival'][e.outVertex().id()] : e.value('start_time') ; m"))
                                    .sack(Lambda.biFunction("m, e -> m['pre_parent'][e.inVertex().id()] = e.outVertex().id(); m"))
                                    .inV()
                                    .dedup()
                                    .where(without("visitedSet"))
                                    .store("visitedSet")
                                    .sack(Lambda.biFunction("m, v -> m['arrival'][v.id()] =  m['pre_arrival'][v.id()]; m"))
                                    .sack(Lambda.biFunction("m, v -> m['parent'][v.id()] =  m['pre_parent'][v.id()]; m"))
                    );

            List bfsList;

            if (Steps == -1) {
                bfsList = t.tail(1)
                        .sack()
                        .map(Lambda.function("it -> [it.sack()['arrival'], it.sack()['parent']]"))
                        .count()
                        .toList();
            } else {
                bfsList = t.times(Steps)
                        .tail(1)
                        .sack()
                        .map(Lambda.function("it -> [it.sack()['arrival'], it.sack()['parent']]"))
                        .count()
                        .toList();
            }

            end = System.currentTimeMillis();

            logger.log("INFO", "Vertex,Steps,Time(ms): " + SourceID.toString() + "," + Steps.toString() + "," + (end - start));

            avgTime += (end-start);


        }

        logger.log("INFO", "Avg. Time(ms): " + avgTime * 1.0 / Source.size());

        g.close();

    }

}
