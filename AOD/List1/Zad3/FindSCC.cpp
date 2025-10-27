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

bool FindSCCList(AdjListGraph& graph){
    auto start = chrono::high_resolution_clock::now();
    AdjListGraph transposed;
    if(!transposeGraphList(graph, transposed)){
        return false;
    }

    int color[graph.vertices]; // 0 - biały, 1 - szary, 2 - czarny
    int pi[graph.vertices];
    stack<int> S;

    std::function<int(int)> DFSVisit = [&](int u) -> int {
        color[u] = 1;
        for(int v : graph.adjList[u]){
            if(color[v] == 0){
                pi[v] = u;
                DFSVisit(v);
            }
        }
        color[u] = 2;
        S.push(u);
        return 1;
    };

    std::function<int(int, vector<int>&)> DFSVisitTransposed = [&](int u,vector<int>& currentSCC) -> int {
        color[u] = 1;
        currentSCC.push_back(u);
        for(int v : transposed.adjList[u]){
            if(color[v] == 0){
                pi[v] = u;
                DFSVisitTransposed(v,currentSCC);
            }
        }
        return 1;
    };

    //1st DFS
    for(int i = 0; i < graph.vertices; i++){
        color[i] = 0; 
        pi[i] = -1; 
    }

    for(int i = 0; i < graph.vertices; i++){
        if(color[i] == 0){
            DFSVisit(i);
        }
    }

    //2nd DFS
    vector<vector<int>> SCCs; 

    for(int i = 0; i < transposed.vertices; i++){
        color[i] = 0; 
        pi[i] = -1; 
    }

    while(!S.empty()){
        int v = S.top();
        S.pop();
        if(color[v] == 0){
            vector<int> currentSCC;
            DFSVisitTransposed(v,currentSCC);
            SCCs.push_back(currentSCC);
        }
    }

   

    //misc
    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = end - start;
    if (graph.vertices < 200) {
        cout << "Strongly Connected Components:" << endl;
        for (size_t i = 0; i < SCCs.size(); i++) {
            cout << "SCC " << i + 1 << ": ";
            for (int v : SCCs[i]) {
                cout << v + 1 << " "; // Przesunięcie indeksu o +1
            }
            cout << endl;
        }
    } else {
        cout << "Number of SCCs: " << SCCs.size() << endl;
        cout << "Sizes of SCCs: ";
        for (const auto& scc : SCCs) {
            cout << scc.size() << " ";
        }
        cout << endl;
    }
    cout << "SCCFind execution time: " << elapsed.count() << " seconds" << endl;
    return true;

}

bool FindSCCMatrix(AdjMatrixGraph& graph){
    auto start = chrono::high_resolution_clock::now();
    AdjMatrixGraph transposed;
    if(!transposeGraphMatrix(graph, transposed)){
        return false;
    }

    int color[graph.vertices]; // 0 - biały, 1 - szary, 2 - czarny
    stack<int> S;

    std::function<int(int)> DFSVisit = [&](int u) -> int {
        color[u] = 1;
        for(int v = 0; v < graph.vertices; v++){
            if(graph.adjMatrix[u][v] == 1 && color[v] == 0){
                DFSVisit(v);
            }
        }
        S.push(u);
        color[u] = 2;
        return 1;
    };

    std::function<int(int, vector<int>&)> DFSVisitTransposed = [&](int u,vector<int>& currentSCC) -> int {
        color[u] = 1;
        currentSCC.push_back(u);
        for(int v = 0; v < graph.vertices; v++){
            if(transposed.adjMatrix[u][v] == 1 && color[v] == 0){
                DFSVisitTransposed(v,currentSCC);
            }
        }
        return 1;
    };

    //1st DFS
    for(int i = 0; i < graph.vertices; i++){
        color[i] = 0; 
    }


    for(int i = 0; i < graph.vertices; i++){
        if(color[i] == 0){
            DFSVisit(i);
        }
    }
    //2nd DFS
    vector<vector<int>> SCCs;

    for(int i = 0; i < transposed.vertices; i++){
        color[i] = 0;
    }

    while(!S.empty()){
        int v = S.top();
        S.pop();
        if(color[v] == 0){
            vector<int> currentSCC;
            DFSVisitTransposed(v,currentSCC);
            SCCs.push_back(currentSCC);
        }
    }

    //misc
    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = end - start;
    if (graph.vertices < 200) {
        cout << "Strongly Connected Components:" << endl;
        for (size_t i = 0; i < SCCs.size(); i++) {
            cout << "SCC " << i + 1 << ": ";
            for (int v : SCCs[i]) {
                cout << v + 1 << " "; // Przesunięcie indeksu o +1
            }
            cout << endl;
        }
    } else {
        cout << "Number of SCCs: " << SCCs.size() << endl;
        cout << "Sizes of SCCs: ";
        for (const auto& scc : SCCs) {
            cout << scc.size() << " ";
        }
        cout << endl;
    }
    cout << "SCCFind execution time: " << elapsed.count() << " seconds" << endl;
    return true;
}

int main() {

    chrono::high_resolution_clock::now();


    string folder = "3";
    // for(const auto & entry : filesystem::directory_iterator(folder)){
    //     string filename = folder + "/" + entry.path().filename().string();
    //     AdjListGraph g;
    //     cout << filename << ":" << endl;
    //     if (readGraphFromFileToAdjList(filename, g)) {
    //         if(g.isDirectional == false){
    //             cout << "Graph is not directed, no point looking for scc." << endl;
    //         }else{
    //             FindSCCList(g);
    //         }
    //     } else {
    //         cout << "Failed to read graph from file: " << endl << filename << endl;
    //     }
    // }

    for(const auto & entry : filesystem::directory_iterator(folder)){
        string filename = folder + "/" + entry.path().filename().string();
        AdjMatrixGraph g;
        cout << filename << ":" << endl;
        if (readGraphFromFileToAdjMatrix(filename, g)) {
            if(g.isDirectional == false){
                cout << "Graph is not directed,  no point looking for scc." << endl;
            }else{
                FindSCCMatrix(g);
            }
        } else {
            cout << "Failed to read graph from file: " << endl << filename << endl;
        }
    }

    return 1;

}