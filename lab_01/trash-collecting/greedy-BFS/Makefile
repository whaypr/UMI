CXX      = gcc
CXXFLAGS = -Wall -pedantic -g
LIBS     = -lstdc++ -lm
OUT      = exec

SRC     := $(shell find . -name '*.cpp')

$(OUT): $(SRC)
	$(CXX) $(CXXFLAGS) $^ -o $(OUT) $(LIBS)

clean:
	rm -f $(OUT)
	