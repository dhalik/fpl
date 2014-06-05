CC=g++
CC_FLAGS=-Wall

./obj/bond.o: ./src/bond.cc
	$(CC) -I./inc -o $< -c $@

./obj/unit.o: ./tests/BondTest.cc
	$(CC) -I./inc -o $@ -c $<

TEST: ./obj/bond.o ./obj/unit.o
	$(CC) ./obj/* -o unitTest
