#include <iostream>
#include <string>
#include <vector>
#include <fstream>

int main()
{
    std::string line;
    std::ifstream file("./day2.txt");

    int p1_horizontal = 0;
    int p1_depth = 0;

    int p2_aim = 0;
    int p2_horizontal = 0;
    int p2_depth = 0;

    while (std::getline(file, line))
    {
        std::string direction = line.substr(0, line.find(" "));
        int distance = std::stoi(line.substr(line.find(" ") + 1));

        if (direction == "down")
        {
            p1_depth += distance;
            p2_aim += distance;
        }
        else if (direction == "up")
        {
            p1_depth -= distance;
            p2_aim -= distance;
        }
        else if (direction == "forward")
        {
            p1_horizontal += distance;
            p2_depth += distance * p2_aim;
            p2_horizontal += distance;
        }
    }

    std::cout << "Part 1: " << p1_horizontal * p1_depth << "\n";
    std::cout << "Part 2: " << p2_horizontal * p2_depth << "\n";
}