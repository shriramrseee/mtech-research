package in.research.baseline.queries;

import org.apache.tinkerpop.gremlin.driver.Client;
import org.apache.tinkerpop.gremlin.driver.Cluster;
import org.apache.tinkerpop.gremlin.driver.MessageSerializer;
import org.apache.tinkerpop.gremlin.driver.remote.DriverRemoteConnection;
import org.apache.tinkerpop.gremlin.driver.ser.GryoMessageSerializerV1d0;
import org.apache.tinkerpop.gremlin.driver.ser.GryoMessageSerializerV3d0;
import org.apache.tinkerpop.gremlin.process.traversal.Traverser;
import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.GraphTraversalSource;
import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.__;
import org.apache.tinkerpop.gremlin.structure.Vertex;
import org.apache.tinkerpop.gremlin.structure.io.IoRegistry;
import org.apache.tinkerpop.gremlin.structure.io.gryo.GryoMapper;
import org.apache.tinkerpop.gremlin.structure.io.gryo.GryoWriter;
import org.apache.tinkerpop.gremlin.util.function.Lambda;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.function.BiFunction;
import java.util.function.Consumer;

import static org.apache.tinkerpop.gremlin.process.traversal.AnonymousTraversalSource.traversal;
import static org.apache.tinkerpop.gremlin.process.traversal.P.*;
import static org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.__.*;

public class tBFS {

    public static void main(String args[]) throws Exception {

        runBFS();
    }

    private static void runBFS() throws Exception {


        GraphTraversalSource g = traversal().withRemote(DriverRemoteConnection.using("localhost", 8182, "g"));

//        System.out.println(g.withSack(Lambda.supplier("[:]")).V(9306117).outE().limit(2).inV().as("a")
//                .sack(Lambda.biFunction("m, v -> m['arrival'] = [:]; m"))
//                .sack(Lambda.biFunction("m,v -> m['arrival'][v.id()] = v.value('start_time'); m"))
//                .sack().as("b")
//                .select("a", "b")
//                .map(Lambda.function("it -> it.path()"))
//                .toList());

        List bfsPathList = g.withSack(Lambda.supplier("[:]"))
                .V(9306117)
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
                )
                .times(1)
                .tail(1)
                .sack()
                .map(Lambda.function("it -> [it.sack()['arrival'], it.sack()['parent']]"))
                .toList();

//        List bfsPathList = g.V().hasId(eq(9306117)).store("visitedSet").repeat(out().where(not(within("visitedSet"))).store("visitedSet")).emit().path().toList();


        System.out.println(bfsPathList.size());

        for(Object o : bfsPathList){
            System.out.println(o.toString());
        }

        g.close();

        System.exit(0);

    }

}
