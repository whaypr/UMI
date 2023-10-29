#include <iostream>
#include <string>

#include "Maze.hpp"
#include "PathFinders/AbstractPathFinder.hpp"
#include "PathFinders/GreedyBFSPathFinder.hpp"

using namespace std;


void crash(string msg, int status) {
    cout << msg << endl;
    exit(status);
}


int main(int argc, char *argv[]) {
    string help =
        "\nexec <input_path>\n";

    if (argc != 2) crash(help, 1);

    ifstream infile(argv[1]);
    if (infile.fail()) {
        infile.close();
        crash("Maze failed to load", 2);
    }

    Maze *maze = nullptr;
    try {
        maze = new Maze(infile);
    } catch (string e) {
        delete maze;
        crash("Error during maze creation: " + e, 3);
    }

    AbstractPathFinder *pathFinder = new GreedyBFSPathFinder(*maze);

    pathFinder->find();

    delete pathFinder;
    delete maze;

    return 0;
}

