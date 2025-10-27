#include <iostream>
#include <fstream>
#include <vector>
#include <string>

using namespace std;

struct AdjListGraph {
    int vertices; // Liczba wierzchołków
    int edges;    // Liczba krawędzi
    bool isDirectional; // Czy graf jest skierowany
    vector<vector<int>> adjList; // Lista sąsiedztwa
};

struct AdjMatrixGraph
{
    int vertices;
    int edges;
    bool isDirectional; 
    vector<vector<int>> adjMatrix; 
};


bool readGraphFromFileToAdjList(const string& filename, AdjListGraph& graph) {
    ifstream file(filename);
    if (!file.is_open()) {
        cout << "Could not open file " << filename << endl;
        return false;
    }

    char directionality;
    file >> directionality;
    graph.isDirectional = (directionality == 'D');

    file >> graph.vertices >> graph.edges;

    // Inicjalizacja listy sąsiedztwa
    graph.adjList.resize(graph.vertices);

    int src, dest;
    for (int i = 0; i < graph.edges; ++i) {
        file >> src >> dest;
        src--; // Przesunięcie indeksu z 1-based na 0-based
        dest--; // Przesunięcie indeksu z 1-based na 0-based
        graph.adjList[src].push_back(dest);
        if (!graph.isDirectional) {
            graph.adjList[dest].push_back(src);
        }
    }

    file.close();
    return true;
}

bool readGraphFromFileToAdjMatrix(const string& filename, AdjMatrixGraph& graph) {
    ifstream file(filename);
    if (!file.is_open()) {
        cout << "Could not open file " << filename << endl;
        return false;
    }

    char directionality;
    file >> directionality;
    graph.isDirectional = (directionality == 'D');

    file >> graph.vertices >> graph.edges;

    // Inicjalizacja macierzy sąsiedztwa
    graph.adjMatrix.resize(graph.vertices, vector<int>(graph.vertices, 0));

    int src, dest;
    for (int i = 0; i < graph.edges; ++i) {
        file >> src >> dest;
        src--; // Przesunięcie indeksu z 1-based na 0-based
        dest--; // Przesunięcie indeksu z 1-based na 0-based
        graph.adjMatrix[src][dest] = 1;
        if (!graph.isDirectional) {
            graph.adjMatrix[dest][src] = 1;
        }
    }

    file.close();
    return true;
}

void printGraphFromAdjList(const AdjListGraph& graph) {
    cout << "Graph: " << endl;
    cout << "Vertices: " << graph.vertices << ", Edges: " << graph.edges << endl;
    cout << "Directional: " << (graph.isDirectional ? "Yes" : "No") << endl;

    for (int i = 0; i < graph.vertices; ++i) {
        cout << "Vertex " << (i + 1) << ":"; // Przesunięcie indeksu o +1
        for (int neighbor : graph.adjList[i]) {
            cout << " " << (neighbor + 1); // Przesunięcie indeksu o +1
        }
        cout << endl;
    }
}

void printGraphFromAdjMatrix(const AdjMatrixGraph& graph) {
    cout << "Graph: " << endl;
    cout << "Vertices: " << graph.vertices << ", Edges: " << graph.edges << endl;
    cout << "Directional: " << (graph.isDirectional ? "Yes" : "No") << endl;

    for (int i = 0; i < graph.vertices; ++i) {
        cout << "Vertex " << (i + 1) << ":"; // Przesunięcie indeksu o +1
        for (int j = 0; j < graph.vertices; ++j) {
            if (graph.adjMatrix[i][j]) {
                cout << " " << (j + 1); // Przesunięcie indeksu o +1
            }
        }
        cout << endl;
    }
}

bool transposeGraphList(AdjListGraph& graph, AdjListGraph& transposed) {
    transposed.adjList.clear();
    transposed.vertices = graph.vertices;
    transposed.edges = graph.edges;
    if(graph.isDirectional == false) {
        cout << "Graph is not directed, no point transposing." << endl;
        return false;
    }
    transposed.isDirectional = graph.isDirectional;

    for(int i = 0; i < graph.vertices; i++){
        transposed.adjList.push_back(vector<int>());
    }

    for(int u = 0; u < graph.vertices; u++){
        for(int v : graph.adjList[u]){
            transposed.adjList[v].push_back(u);
        }
    }
    return true;
}

bool transposeGraphMatrix(AdjMatrixGraph& graph, AdjMatrixGraph& transposed) {
    transposed.adjMatrix.clear();
    transposed.vertices = graph.vertices;
    transposed.edges = graph.edges;
    if(graph.isDirectional == false) {
        cout << "Graph is not directed, no point transposing." << endl;
        return false;
    }
    transposed.isDirectional = graph.isDirectional;

    transposed.adjMatrix.resize(graph.vertices, vector<int>(graph.vertices, 0));
    for(int i = 0; i < graph.vertices; i++){
        for(int j = 0; j < graph.vertices; j++){
            transposed.adjMatrix[j][i] = graph.adjMatrix[i][j];
        }
    }
    return true;
}

// int main() {
//     AdjListGraph graph;
//     if (readGraphFromFileToAdjList("g2a-1.txt", graph)) {
//         printGraphFromAdjList(graph);
//     } else {
//         cerr << "Failed to load graph." << endl;
//     }

//     return 0;
// }