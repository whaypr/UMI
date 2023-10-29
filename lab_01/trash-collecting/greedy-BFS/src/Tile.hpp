#pragma once

#include <cstdint>
#include <fstream>
#include "State.hpp"

struct Tile {
    Tile(State state, int x, int y, int startDistance = INT32_MAX, double endDistanceHeuristic = INT32_MAX, Tile *predecessor = nullptr)
        : state(state), x(x), y(y), startDistance(startDistance), endDistanceHeuristic(endDistanceHeuristic), predecessor(predecessor) {}

    State state;
    int x, y, startDistance;
    double endDistanceHeuristic;
    Tile *predecessor;

    friend std::ostream& operator<<(std::ostream& os, const Tile& t) {
        os << "(" << t.x << "," << t.y << ")";
        return os;
    }
};
