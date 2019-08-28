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

public class tDFS {

    private Graph graph;
    private Log logger;

    public tDFS(Graph g) throws IOException {
        graph = g;
        logger = new Log();
    }

    public List runDFS(Long SourceID, Integer Steps) throws Exception {


        GraphTraversalSource g = (GraphTraversalSource) graph.getGraph();

        logger.log("INFO", "Start tDFS for Vertex,Steps: " + SourceID.toString() + "," + Steps.toString());

        GraphTraversal<Vertex, Vertex> t = g.withSack(Lambda.supplier("[:]"))
                .V(SourceID)
                .store("visitedSet")
                .sack(Lambda.biFunction("m, v -> m['arrival'] = [:]; m"))
                .sack(Lambda.biFunction("m, v -> m['parent'] = [:]; m"))
                .sack(Lambda.biFunction("m, v -> m['pre_arrival'] = [:]; m"))
                .sack(Lambda.biFunction("m, v -> m['pre_parent'] = [:]; m"))
                .sack(Lambda.biFunction("m, v -> m['stack'] = []; m"))
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
                        .sack(Lambda.biFunction("m, v -> m['stack'].push(v); m"))
                        .tail(1)
                        .repeat(
                            repeat(
                                V(SourceID)
                                .sideEffect( sack().as("x")
                                    .select("x")
                                    .map(Lambda.function("it -> it.sack()['stack'].size() > 0 ? it.sack()['stack'].pop() : null")).store("vnext")
                                )
                                .sideEffect( sack().as("x")
                                    .select("x")
                                    .sideEffect(Lambda.consumer("println it.sack()['stack']"))
                                )
                                .V()
                                .where(within("vnext"))
                            )
                                .times(1)
//                            .until(where(without("visitedSet")))
                            .store("visitedSet")
                            .sack(Lambda.biFunction("m, v -> m['arrival'][v.id()] =  m['pre_arrival'][v.id()]; m"))
                            .sack(Lambda.biFunction("m, v -> m['parent'][v.id()] =  m['pre_parent'][v.id()]; m"))
                            .sideEffect(Lambda.consumer("println it"))
                        )
                        .times(4)
//                        .until(where(outE().count().is(gt(0))))

                );

        List dfsList;

        if (Steps == -1) {
            dfsList = t.tail(1)
                    .sack()
                    .map(Lambda.function("it -> [it.sack()['arrival'], it.sack()['parent']]"))
                    .toList();
        } else {
            dfsList = t.times(Steps)
                    .tail(1)
                    .sack()
                    .map(Lambda.function("it -> [it.sack()['arrival'], it.sack()['parent']]"))
                    .toList();
        }

        logger.log("INFO", "Finish tDFS for Vertex,Steps: " + SourceID.toString() + "," + Steps.toString());

        g.close();

        return dfsList;

    }

}
