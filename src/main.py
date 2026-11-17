"""Pipeline entry point: parse input, run OR-tree search, hill climb, write output."""

from model.parser import readInput

def main():
    data = readInput('./inputs/input.txt')
    print(data)

if __name__ == "__main__":
    main()
