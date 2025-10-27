#ifndef AOD_H
#define AOD_H
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

bool readGraphFromFileToAdjList(const string& filename, AdjListGraph& graph);
bool readGraphFromFileToAdjMatrix(const string& filename, AdjMatrixGraph& graph);
void printGraphFromAdjList(const AdjListGraph& graph);
void printGraphFromAdjMatrix(const AdjMatrixGraph& graph);
bool transposeGraphList(AdjListGraph& graph, AdjListGraph& transposed);
bool transposeGraphMatrix(AdjMatrixGraph& graph, AdjMatrixGraph& transposed);

#endif 