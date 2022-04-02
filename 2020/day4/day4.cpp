#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <array>
#include <algorithm>
#include <numeric>

class Field
{
public:
    std::string name;
    std::string value;
    bool valid;

    Field(std::string name, std::string value, bool (*validate)(std::string, std::vector<int>), std::vector<int> criteria)
    {
        this->name = name;
        this->value = value;
        this->valid = validate(value, criteria);
    }
};

std::string trim(std::string str)
{
    str.erase(remove(str.begin(), str.end(), ' '), str.end());

    return str;
}

bool NoValidator(std::string value, std::vector<int> criteria)
{
    return true;
}

bool RangeValidator(std::string value, std::vector<int> criteria)
{
    int min = criteria[0];
    int max = criteria[1];

    try
    {
        int num = std::stoi(value);

        if (num >= min && num <= max)
        {
            return true;
        }
        else
        {
            return false;
        }
    }
    catch (std::invalid_argument)
    {
        return false;
    }
}

bool HeightValidator(std::string value, std::vector<int> criteria)
{
    int cmMin = criteria[0];
    int cmMax = criteria[1];
    int inMin = criteria[2];
    int inMax = criteria[3];

    if (value.find("in") != std::string::npos)
    {
        std::string in = value.substr(0, value.find("in"));
        return RangeValidator(in, {inMin, inMax});
    }
    else
    {
        std::string cm = value.substr(0, value.find("cm"));
        return RangeValidator(cm, {cmMin, cmMax});
    }
}

bool HairColorValidator(std::string value, std::vector<int> criteria)
{
    value = trim(value);

    if (value.size() != 7)
    {
        return false;
    }
    return true;
}

bool EyeColorValidator(std::string value, std::vector<int> criteria)
{
    value = trim(value);
    std::vector<std::string> options = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"};
    return std::find(options.begin(), options.end(), value) != options.end();
}

bool PIDValidator(std::string value, std::vector<int> criteria)
{
    value = trim(value);

    if (value.size() != 9)
    {
        return false;
    }
    return true;
}

int main()
{
    std::vector<std::string> data;
    std::string temp;
    std::string line;
    std::ifstream File("./test.txt");

    while (getline(File, line))
    {
        if (temp == "")
        {
            temp = line;
        }
        else if (line == "")
        {
            data.push_back(temp);
            temp = "";
        }
        else
        {
            temp += line;
        }
    }
    data.push_back(temp);

    std::array<std::string, 8> fieldNames = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"};

    int valid = 0;
    int c = 0;

    // std::string entry = data[10];
    for (auto &entry : data)
    {
        std::vector<Field> fields;
        // std::cout << entry << "\n\n";
        std::vector<int> positions;

        bool done = false;
        // while (!done)
        // {
        // find positions of all colons
        for (int i = 0; i < entry.size(); i++)
        {
            if (entry[i] == ':')
            {
                positions.push_back(i - 3);
            }
        }
        // }
        // for (auto &field : fieldNames)
        // {
        //     if (entry.find(field) == std::string::npos)
        //     {
        //         // missing.push_back(field);
        //         valid = false;
        //     }
        //     else
        //     {
        //         // std::cout << entry.substr(entry.find(field) + 4, 4) << "\n";
        //         // std::cout << entry.substr(entry.find(field)) << "\n";
        //         positions.push_back(entry.find(field));
        //     }
        // }

        sort(positions.begin(), positions.end());

        // print positions
        for (auto &pos : positions)
        {
            // std::cout << pos << " ";
        }
        // std::cout << "\n";

        for (int i = 0; i < positions.size(); i++)
        {
            std::string str{};
            if (i != positions.size() - 1)
            {
                str = entry.substr(positions[i], positions[i + 1] - positions[i]);
            }
            else
            {
                str = entry.substr(positions[i], positions[i + 1] - entry.length());
            }
            std::string name = str.substr(0, str.find(":"));
            // std::cout << x << "\n";

            if (str.find("cid") == std::string::npos)
            {
                bool (*validate)(std::string, std::vector<int>) = NULL;
                std::vector<int> criteria;
                bool c = true;

                if (name == "byr")
                {
                    validate = RangeValidator;
                    criteria = {1920, 2002};
                }
                else if (name == "iyr")
                {
                    validate = RangeValidator;
                    criteria = {2010, 2020};
                }
                else if (name == "eyr")
                {
                    validate = RangeValidator;
                    criteria = {2020, 2030};
                }
                else if (name == "hgt")
                {
                    validate = HeightValidator;
                    criteria = {150, 193, 59, 76};
                }
                else if (name == "hcl")
                {
                    validate = HairColorValidator;
                    criteria = {};
                }
                else if (name == "ecl")
                {
                    validate = EyeColorValidator;
                    criteria = {};
                }
                else if (name == "pid")
                {
                    validate = PIDValidator;
                    criteria = {};
                }
                else
                {
                    c = false;
                }

                if (c)
                {
                    fields.push_back(Field(name, str.substr(str.find(":") + 1), validate, criteria));
                }
            }
        }

        if (std::accumulate(fields.begin(), fields.end(), 0, [](int acc, Field field)
                            { return acc + field.valid; }) == 7)
        {
            valid++;
            c++;
        }
        else
        {
            std::cout << entry << " INVALID\n";
        }

        // print fields
        for (auto &field : fields)
        {
            std::cout << field.name << ": " << field.value << " " << field.valid << "\n";
        }
        std::cout << "\n";
    }

    std::cout << c << std::endl;

    return 0;
}