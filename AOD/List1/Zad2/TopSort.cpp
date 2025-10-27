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

bool TopSortList(AdjListGraph& graph,int startVertex){
    auto start = chrono::high_resolution_clock::now();

    int color[graph.vertices]; // 0 - biały, 1 - szary, 2 - czarny
    int d[graph.vertices];
    int pi[graph.vertices];
    int time = 0;
    stack<int> S;

    std::function<int(int)> DFSVisit = [&](int u) -> int {
        color[u] = 1;
        time++;
        d[u] = time;
        // if(print == 1){cout << "Visiting vertex: " << (u + 1) << endl;}
        for(int v : graph.adjList[u]){
            if(color[v] == 0){
                pi[v] = u;
                if(DFSVisit(v) == 0) return 0;
            }else if(color[v] == 1){
                return 0;
            }
        }
        color[u] = 2;
        S.push(u);
        time++;
        return 1;
    };

    for(int i = 0; i < graph.vertices; i++){
        color[i] = 0; 
        pi[i] = -1; 
    }

    for(int i = 0; i < graph.vertices; i++){
        if(color[i] == 0){
            if(DFSVisit(i)==0) { 
                cout << "Graph has a cycle" << endl;
                auto end = chrono::high_resolution_clock::now();
                chrono::duration<double> elapsed = end - start;
                cout << "TopSort execution time: " << elapsed.count() << " seconds" << endl;
                return false;
            }
        }
    }

    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = end - start;
    if(graph.vertices < 200){
        cout << "Topological Sort Order: ";
        while(!S.empty()){
            cout << S.top() + 1 << " "; // Przesunięcie indeksu o +1
            S.pop();
        }
        cout << endl;
    }
    cout << "TopSort execution time: " << elapsed.count() << " seconds" << endl;
    return true;
}

bool TopSortMatrix(AdjMatrixGraph& graph,int startVertex){
    auto start = chrono::high_resolution_clock::now();

    int color[graph.vertices]; // 0 - biały, 1 - szary, 2 - czarny
    int d[graph.vertices];
    int pi[graph.vertices];
    int time = 0;
    stack<int> S;

    std::function<int(int)> DFSVisit = [&](int u) -> int {
        color[u] = 1;
        time++;
        d[u] = time;
        // if(print == 1){cout << "Visiting vertex: " << (u + 1) << endl;}
        for(int v = 0; v < graph.vertices; v++){
            if(graph.adjMatrix[u][v] == 1){
                if(color[v] == 0){
                    pi[v] = u;
                    if(DFSVisit(v) == 0) return 0;
                }else if(color[v] == 1){
                    return 0;
                }
            }
        }
        color[u] = 2;
        S.push(u);
        time++;
        return 1;
    };

    for(int i = 0; i < graph.vertices; i++){
        color[i] = 0; 
        pi[i] = -1; 
    }

    for(int i = 0; i < graph.vertices; i++){
        if(color[i] == 0){
            if(DFSVisit(i)==0) { 
                cout << "Graph has a cycle" << endl;
                auto end = chrono::high_resolution_clock::now();
                chrono::duration<double> elapsed = end - start;
                cout << "TopSort execution time: " << elapsed.count() << " seconds" << endl;
                return false;
            }
        }
    }

    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = end - start;
    if(graph.vertices < 200){
        cout << "Topological Sort Order: ";
        while(!S.empty()){
            cout << S.top() + 1 << " "; // Przesunięcie indeksu o +1
            S.pop();
        }
        cout << endl;
    }
    cout << "TopSort execution time: " << elapsed.count() << " seconds" << endl;
    return true;
}

int main(int argc, char* argv[]) {

    chrono::high_resolution_clock::now();
    if(argc != 2){
        cout << "Usage: " << argv[0] << " <start_vertex>" << endl;
        return 1;
    }

    string folder = "2";
    for(const auto & entry : filesystem::directory_iterator(folder)){
        string filename = folder + "/" + entry.path().filename().string();
        AdjListGraph g;
        cout << filename << ":" << endl;
        if (readGraphFromFileToAdjList(filename, g)) {
            // cout << "Graph from file " << filename << ":\n";
            // printGraphFromAdjList(graph[i]);
            // cout << endl;
            if(g.isDirectional == false){
                cout << "Graph is not directed, topological sort not possible." << endl;
            }else{
                TopSortList(g, atoi(argv[1])-1);
            }
        } else {
            cout << "Failed to read graph from file: " << endl << filename << endl;
        }
    }

    for(const auto & entry : filesystem::directory_iterator(folder)){
        string filename = folder + "/" + entry.path().filename().string();
        AdjMatrixGraph g;
        cout << filename << ":" << endl;
        if (readGraphFromFileToAdjMatrix(filename, g)) {
            // cout << "Graph from file " << filename << ":\n";
            // printGraphFromAdjMatrix(graphM[i]);
            // cout << endl;
            if(g.isDirectional == false){
                cout << "Graph is not directed, topological sort not possible." << endl;
            }else{
                TopSortMatrix(g, atoi(argv[1])-1);
            }
        } else {
            cout << "Failed to read graph from file: " << endl << filename << endl;
        }
    }
    return 1;

}