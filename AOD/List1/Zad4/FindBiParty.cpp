#include <bits/stdc++.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <chrono>
#include <stack>
#include <climits>
#include <functional>
#include <filesystem>
#include "aod.h"

using namespace std;

bool IsBiPartyList(AdjListGraph& graph){
    auto start = chrono::high_resolution_clock::now();

    int color[graph.vertices]; // 0 - unvisited, 1 - white, 2 - black


    std::function<int(int)> DFSVisit = [&](int u) -> int {
        for (int v : graph.adjList[u]) {
            if (color[v] == 0) {
                color[v] = 3 - color[u]; // przeciwstawny kolor
                if (DFSVisit(v) == -1) return -1;
            } else if (color[v] == color[u]) {
                return -1; // konflikt kolorów → niedwudzielny
            }
        }
        return 1;
    };

    for(int i = 0; i < graph.vertices; i++){
        color[i] = 0;  
    }

    for (int i = 0; i < graph.vertices; i++) {
        if (color[i] == 0) {
            color[i] = 1;
            if (DFSVisit(i) == -1) {
                cout << "Graph is not bipartite." << endl;
                auto end = chrono::high_resolution_clock::now();
                chrono::duration<double> elapsed = end - start;
                cout << "Bipartite check execution time: " << elapsed.count() << " seconds" << endl;
                return false;
            }
        }
    }

    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = end - start;
    cout << "Graph is bipartite." << endl;
    cout << "Bipartite check execution time: " << elapsed.count() << " seconds" << endl;
    return true;
}

bool IsBiPartyMatrix(AdjMatrixGraph& graph){
    auto start = chrono::high_resolution_clock::now();

    int color[graph.vertices]; // 0 - unvisited, 1 - white, 2 - black
    std::function<int(int)> DFSVisit = [&](int u) -> int {
        for (int v = 0; v < graph.vertices; v++) {
            if (graph.adjMatrix[u][v] == 1) {
                if (color[v] == 0) {
                    color[v] = 3 - color[u]; // przeciwstawny kolor
                    if (DFSVisit(v) == -1) return -1;
                } else if (color[v] == color[u]) {
                    return -1; // konflikt kolorów → niedwudzielny
                }
            }
        }
        return 1;
    };

    for(int i = 0; i < graph.vertices; i++){
        color[i] = 0;  
    }

    for (int i = 0; i < graph.vertices; i++) {
        if (color[i] == 0) {
            color[i] = 1;
            if (DFSVisit(i) == -1) {
                cout << "Graph is not bipartite." << endl;
                auto end = chrono::high_resolution_clock::now();
                chrono::duration<double> elapsed = end - start;
                cout << "Bipartite check execution time: " << elapsed.count() << " seconds" << endl;
                return false;
            }
        }
    }

    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = end - start;
    cout << "Graph is bipartite." << endl;
    cout << "Bipartite check execution time: " << elapsed.count() << " seconds" << endl;
    return true;
}

int main() {

    chrono::high_resolution_clock::now();


    string folder = "4";
    // for(const auto & entry : filesystem::directory_iterator(folder)){
    //     string filename = folder + "/" + entry.path().filename().string();
    //     AdjListGraph g;
    //     cout << filename << ":" << endl;
    //     if (readGraphFromFileToAdjList(filename, g)) {
    //         IsBiPartyList(g);
    //     } else {
    //         cout << "Failed to read graph from file: " << endl << filename << endl;
    //     }
    // }

    for(const auto & entry : filesystem::directory_iterator(folder)){
        string filename = folder + "/" + entry.path().filename().string();
        AdjMatrixGraph g;
        cout << filename << ":" << endl;
        if (readGraphFromFileToAdjMatrix(filename, g)) {
            IsBiPartyMatrix(g);
        } else {
            cout << "Failed to read graph from file: " << endl << filename << endl;
        }
    }

    return 1;

}