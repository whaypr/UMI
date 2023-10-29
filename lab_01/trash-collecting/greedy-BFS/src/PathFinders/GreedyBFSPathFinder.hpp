#pragma once

#include <queue>
#include <iostream>
#include "AbstractPathFinder.hpp"

using namespace std;


class GreedyBFSPathFinder : public AbstractPathFinder {
public:
  
  GreedyBFSPathFinder(Maze &maze) : AbstractPathFinder(maze) {}


  // ------------------------------------------------------------------------------
  void find() override {
    maze.printMaze();
    // iterate until there are all trashes picked
    // in each iteration pick greedily the closest trash
    while (!maze.ends.empty()) {
        bool found = false;
        queue<Tile*> open;
        open.push(&maze.layout[maze.startY][maze.startX]);

        int kek = 1;

        while (!open.empty()) {
            Tile *t = open.front();
            open.pop();

            auto it = maze.ends.find(make_pair(t->x, t->y));
            if (it != maze.ends.end()) {
                found = true;
                maze.printMaze(t->x, t->y, false);
                maze.ends.erase(it);
                maze.startX = t->x;
                maze.startY = t->y;
                break;
            }

            for (pair<int, int> p : {make_pair(t->x-1, t->y), make_pair(t->x+1, t->y), make_pair(t->x, t->y-1), make_pair(t->x, t->y+1)}) {
                Tile *tNext = &maze.layout[p.second][p.first];
                if (tNext->state == undiscovered) {
                    tNext->predecessor = t;
                    tNext->state = opened;
                    open.push(tNext);
                    kek++;
                }
            }

            t->state = closed;
        }

        if (!found)
            throw "ERROR!";

        maze.resetMaze();
    }

    maze.printMaze(-1, -1, false);
    maze.printMaze();
  }

};
