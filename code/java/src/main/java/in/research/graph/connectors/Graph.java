package in.research.graph.connectors;

public class Graph<G> {

    private G instance;

    Graph(G graph) {
        instance = graph;
    }

    public G getGraph() {
        return instance;
    }

}
