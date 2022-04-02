#include <iostream>
#include <string>
#include <vector>
#include <fstream>

int main()
{
    std::vector<int> depths;
    std::string line;
    std::fstream file("./day1.txt");

    while (std::getline(file, line))
    {
        depths.push_back(std::stoi(line));
    }
    file.close();

    int count = -1;
    int prev = 0;

    for (auto &depth : depths)
    {
        if (depth > prev)
        {
            count++;
        }
        prev = depth;
    }

    std::cout << "Part 1: " << count << "\n";

    count = -1;
    prev = 0;

    for (int i = 0; i < depths.size(); i++)
    {
        int sum = depths[i] + depths[i + 1] + depths[i + 2];

        if (sum > prev)
        {
            count++;
        }
        prev = sum;
    }

    std::cout << "Part 2: " << count << "\n";
}