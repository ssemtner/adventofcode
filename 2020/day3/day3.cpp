#include <iostream>
#include <vector>
#include <string>
#include <fstream>

int calculateTreesHit(const std::vector<std::vector<bool>> &data, const int dx, const int dy)
{
    int x = 0;
    int y = 0;

    int trees = 0;

    while (y < data.size() - 1)
    {
        x += dx;
        y += dy;

        if (x >= data[0].size())
        {
            x -= data[0].size();
        }

        if (data[y][x])
        {
            trees++;
        }
    }

    return trees;
}

int main()
{
    std::vector<std::vector<bool>> data;
    std::string line;
    std::ifstream File("./day3.txt");

    while (getline(File, line))
    {
        std::vector<bool> temp;
        for (auto &c : line)
        {
            temp.push_back(c == '#');
        }
        data.push_back(temp);
    }

    std::cout << "Part 1: " << calculateTreesHit(data, 3, 1) << std::endl;

    int slopes[5][2] = {{1, 1}, {3, 1}, {5, 1}, {7, 1}, {1, 2}};
    long product = 1;

    for (auto slope : slopes)
    {
        std::cout << slope[0] << " " << slope[1] << " " << calculateTreesHit(data, slope[0], slope[1]) << "\n";
        product *= calculateTreesHit(data, slope[0], slope[1]);
    }

    std::cout << "Part 2: " << product << std::endl;

    return 0;
}