#pragma once
#include "../Maze.hpp"

class AbstractPathFinder {
public:
  
    AbstractPathFinder(Maze& maze): maze(maze) {}
    virtual void find() {}

    
protected:
    
  Maze& maze;    
};
