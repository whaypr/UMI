#pragma once

#include <vector>
#include <cstdint>
#include <set>
#include <iostream>
#include <string>
#include <sstream>
#include "State.hpp"
#include "Tile.hpp"

using namespace std;


class Maze {
public:
  
  Maze(std::ifstream &infile) {
    string line;
    int row = 0;

    while (getline(infile, line)) {
        layout.push_back({});

        istringstream iss(line);
        int col = 0;

        char c;
        iss.get(c);
        while (!iss.eof()) {
            if (c == 'X') {
                layout[row].push_back(Tile(wall, col, row));
            } else if (c == ' ') {
                layout[row].push_back(Tile(undiscovered, col, row));
            } else if (c == 'R') {
                layout[row].push_back(Tile(undiscovered, col, row));
                startX = col;
                startY = row;
            } else if (c == 'T') {
                layout[row].push_back(Tile(undiscovered, col, row));
                ends.insert(make_pair(col, row));
            } else {
                throw "ERROR!";
            }

            iss.get(c);
            col++;
        }

        row++;
    }
  }


  // ------------------------------------------------------------------------------
  void resetMaze() {
    for ( auto & row: layout ) {
        for (Tile &t : row) {
            if (t.state == closed || t.state == opened || t.state == path)
                t.state = undiscovered;
            t.predecessor = nullptr;
            t.startDistance = INT32_MAX;
            t.endDistanceHeuristic = INT32_MAX;
        }
    }
  }


  // ------------------------------------------------------------------------------
  void printMaze(int endX = -1, int endY = -1, bool startOrEnd = true) {
    // prepare the path
    int tmpPathLen = 0;
    if (endX != -1) {
        Tile *pred = layout[endY][endX].predecessor;
        completePath.insert(make_pair(endX, endY));
        while (pred) {
            tmpPathLen++;
            pred->state = path;
            completePath.insert(make_pair(pred->x, pred->y));
            pred = pred->predecessor;
        }
    }

    // print out the maze
    for ( const auto & row: layout ) {
        for (const auto & t : row) {
            if (t.x == startX && t.y == startY && (!startOrEnd || completePath.size() == 0)) {
                cout << "\033[1;31mR\033[0m";
                continue;
            }
            if (startOrEnd && completePath.find(make_pair(t.x, t.y)) != completePath.end()) {
                cout << "\033[1;31m.\033[0m";
                continue;
            }
            if ( (t.x == endX && t.y == endY) ) {
                cout << "\033[1;31mT\033[0m";
                continue;
            }
            if ( ends.find(make_pair(t.x, t.y)) != ends.end() ) {
                cout << "\033[1;33mT\033[0m";
                continue;
            }

            switch (t.state) {
                case wall:
                    cout << "\033[1;32mX\033[0m";
                    break;
                case closed:
                case opened:
                case undiscovered:
                    cout << " ";
                    break;
                case path:
                    cout << "\033[1;31m.\033[0m";
                    break;
            }
        }
        cout << endl;
    }

    // continue prompt
    std::cout << "Trashes remaining: " << ends.size() << std::endl;
    std::cout << "Traveled so far: " << pathTotalLen << std::endl;
    std::cout << "Press enter to continue" << std::endl;
    pathTotalLen += tmpPathLen;
    getchar();
  }


  std::vector<std::vector<Tile>> layout;
  int startX, startY;
  std::set<std::pair<int, int>> ends;
  std::set<std::pair<int, int>> completePath;
  int pathTotalLen = 0;
  
};
