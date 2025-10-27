#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <chrono>
#include <queue>
#include <climits>
#include <functional>
#include "aod.h"

using namespace std;

bool dfsList(AdjListGraph& graph,int startVertex,int print){
    auto start = chrono::high_resolution_clock::now();

    int color[graph.vertices]; // 0 - biały, 1 - szary, 2 - czarny
    int d[graph.vertices];
    int pi[graph.vertices];
    int time = 0;

    std::function<int(int)> DFSVisit = [&](int u) -> int {
        color[u] = 1;
        time++;
        d[u] = time;
        if(print == 1){cout << "Visiting vertex: " << (u + 1) << endl;}
        for(int v : graph.adjList[u]){
            if(color[v] == 0){
                pi[v] = u;
                DFSVisit(v);
            }
        }
        color[u] = 2;
        time++;
        return 1;
    };

    for(int i = 0; i < graph.vertices; i++){
        color[i] = 0; 
        pi[i] = -1; 
    }

    for(int i = 0; i < graph.vertices; i++){
        if(color[i] == 0){
            DFSVisit(i);
        }
    }

    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = end - start;
    cout << "DFS execution time: " << elapsed.count() << " seconds" << endl;
    return true;
}

bool dfsMatrix(AdjMatrixGraph& graph,int startVertex,int print){
    auto start = chrono::high_resolution_clock::now();

    int color[graph.vertices]; // 0 - biały, 1 - szary, 2 - czarny
    int d[graph.vertices];
    int pi[graph.vertices];
    int time = 0;

    std::function<int(int)> DFSVisit = [&](int u) -> int {
        color[u] = 1;
        time++;
        d[u] = time;
        if(print == 1){cout << "Visiting vertex: " << (u + 1) << endl;}
        for(int v = 0; v < graph.vertices; v++){
            if(graph.adjMatrix[u][v] == 1 && color[v] == 0){
                pi[v] = u;
                DFSVisit(v);
            }
        }
        color[u] = 2;
        time++;
        return 1;
    };

    for(int i = 0; i < graph.vertices; i++){
        color[i] = 0; 
        pi[i] = -1; 
    }

    for(int i = 0; i < graph.vertices; i++){
        if(color[i] == 0){
            DFSVisit(i);
        }
    }

    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = end - start;
    cout << "DFS execution time: " << elapsed.count() << " seconds" << endl;
    return true;
}

int main(int argc, char* argv[]){

    chrono::high_resolution_clock::now();
    if(argc != 3){
        cerr << "Usage: " << argv[0] << " <start_vertex> <print_tree_?_1/0>" << endl;
        return 1;
    }

    struct AdjListGraph graph[8];

    for(int i = 0; i < 8; i++){
        string filename = "graphs/g-" + to_string(i+1) + ".txt";
        if (readGraphFromFileToAdjList(filename, graph[i])) {
            // cout << "Graph from file " << filename << ":\n";
            // printGraphFromAdjList(graph[i]);
            // cout << endl;
            dfsList(graph[i], atoi(argv[1])-1,atoi(argv[2]));
        } else {
            cerr << "Failed to read graph from file " << filename << endl;
        }
    }

    struct AdjMatrixGraph graphM[8];
    
    for(int i = 0; i < 8; i++){
        string filename = "graphs/g-" + to_string(i+1) + ".txt";
        if (readGraphFromFileToAdjMatrix(filename, graphM[i])) {
            // cout << "Graph from file " << filename << ":\n";
            // printGraphFromAdjMatrix(graphM[i-1]);
            // cout << endl;
            dfsMatrix(graphM[i], atoi(argv[1])-1,atoi(argv[2]));
        } else {
            cerr << "Failed to read graph from file " << filename << endl;
        }
    }

}