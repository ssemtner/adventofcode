#include <iostream>
#include <string>
#include <fstream>
#include <vector>

int part1(std::vector<int> &input)
{
	for (auto x : input)
	{
		for (auto y : input)
		{
			if (x + y == 2020)
			{
				return x * y;
			}
		}
	}

	return 0;
}

int part2(std::vector<int> &input)
{
	for (auto x : input)
	{
		for (auto y : input)
		{
			for (auto z : input)
			{
				if (x + y + z == 2020)
				{
					return x * y * z;
				}
			}
		}
	}

	return 0;
}

int main()
{
	std::vector<int> data;
	std::string line;
	std::ifstream File("./input.txt");

	while (getline(File, line))
	{
		data.push_back(std::stoi(line));
	}

	File.close();

	std::cout << "Part 1: " << part1(data) << std::endl;
	std::cout << "Part 2: " << part2(data) << std::endl;

	return 0;
}
