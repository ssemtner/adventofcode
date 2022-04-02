#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <algorithm>

struct password
{
    int min;
    int max;
    char letter;
    std::string password;
};

int part1(std::vector<password> &passwords)
{
    int valid_passwords = 0;
    for (auto &password : passwords)
    {
        int count = std::count(password.password.begin(), password.password.end(), password.letter);
        if (count >= password.min && count <= password.max)
        {
            valid_passwords++;
        }
    }
    return valid_passwords;
}

int part2(std::vector<password> &passwords)
{
    int valid_passwords = 0;
    for (auto &password : passwords)
    {
        if (!(password.password[password.min - 1] == password.letter) != !(password.password[password.max - 1] == password.letter))
        {
            valid_passwords++;
        }
    }
    return valid_passwords;
}

int main()
{
    std::vector<password> passwords;

    std::string line;
    std::ifstream File("./day2.txt");

    while (getline(File, line))
    {
        password temp{};
        temp.min = std::stoi(line.substr(0, line.find("-")));
        temp.max = std::stoi(line.substr(line.find("-") + 1, line.find(" ")));
        temp.letter = line[line.find(" ") + 1];
        temp.password = line.substr(line.find(":") + 2);

        passwords.push_back(temp);
    }

    File.close();

    std::cout << "Part 1: " << part1(passwords) << std::endl;
    std::cout << "Part 2: " << part2(passwords) << std::endl;

    return 0;
}
