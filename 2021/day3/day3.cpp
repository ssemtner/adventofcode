#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <numeric>
#include <algorithm>
#include <sstream>
#include <iterator>

enum filter
{
    MOST_COMMON = false,
    LEAST_COMMON = true,
};

int part2(std::vector<std::vector<int>> set, filter f)
{
    int i = 0;
    int sizeV = set.size();
    int sizeH = set[0].size();
    while (set.size() > 1)
    {
        std::vector<std::vector<int>> newSet;

        int t;
        int sum = 0;
        for (int j = 0; j < set.size(); j++)
        {
            sum += set[j][i];
        }
        if (sum < set.size() * 0.5)
        {
            t = f ? 0 : 1;
        }
        else
        {
            t = f ? 1 : 0;
        }

        std::copy_if(set.begin(), set.end(), std::back_inserter(newSet), [i, t](std::vector<int> s)
                     { return s[i] == t; });

        set = newSet;

        i++;
    }

    std::stringstream ss;
    std::copy(set[0].begin(), set[0].end(), std::ostream_iterator<int>(ss, ""));
    return std::stoi(ss.str(), 0, 2);
}

int main()
{
    std::vector<std::vector<int>> grid;
    std::string line;
    std::ifstream file("./day3.txt");

    while (std::getline(file, line))
    {
        std::vector<int> row;

        for (auto c : line)
        {
            row.push_back(c - 48);
        }

        grid.push_back(row);
    }

    std::string epsilon;

    for (int x = 0; x < grid[0].size(); x++)
    {
        int sum = std::accumulate(grid.begin(), grid.end(), 0, [x](int a, std::vector<int> b)
                                  { return a + b[x]; });

        if (sum > grid.size() * 0.5)
        {
            epsilon += '1';
        }
        else
        {
            epsilon += '0';
        }
    }

    std::string gamma = "";
    for (auto c : epsilon)
    {
        if (c == '1')
        {
            gamma += '0';
        }
        else
        {
            gamma += '1';
        }
    }

    std::cout << "Power Consumption: " << std::stoi(epsilon, 0, 2) * std::stoi(gamma, 0, 2) << "\n";

    std::cout << "Life Support Rating: " << part2(grid, MOST_COMMON) * part2(grid, LEAST_COMMON) << "\n";
}
