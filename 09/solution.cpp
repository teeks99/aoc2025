#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <cstdint>

enum class PointType : uint8_t
{
    UNKNOWN = 0,
    VERTEX = 1,
    WALL = 2,
    INSIDE = 3,
    OUTSIDE = 4,
    RECTANGEL = 5,
    WALL_NORTH = 6,
    WALL_WEST = 7,
    WALL_SOUTH = 8,
    WALL_EAST = 9
};

enum class RectDirection : uint8_t
{
    INVALID = 0,
    NORTH_EAST = 1,
    SOUTH_EAST = 2,
    SOUTH_WEST = 3,
    NORTH_WEST = 4
};

class Solution
{
public:
    Solution(std::string inputFile)
    {
        LoadFile(inputFile);
    }

    void LoadFile(std::string inputFileName)
    {
        std::ifstream inputFile(inputFileName);

        uint32_t val1, val2;
        char delimiter; // To consume the ','

        // The loop continues as long as we successfully read: int -> char -> int
        while (inputFile >> val1 >> delimiter >> val2) {
            // Optional: strict check to ensure the delimiter was actually a comma
            if (delimiter == ',')
            {
                if (val1 > max_x) {max_x = val1;}
                if (val2 > max_y) {max_y = val1;}
                red_coords.emplace_back(val1, val2);
            }
            else
            {
                throw std::runtime_error("Bad file read");
            }
        }

        inputFile.close();        
    }
    void PrintCoords()
    {
        std::cout << "Coordinate Pairs" << std::endl;
        for(auto coords : red_coords)
        {
            std::cout << coords.first << "," << coords.second << std::endl;
        }
    }

    void Run()
    {
        MakeMap();
        MakeWalls();
        MakeRectangles();
    }
    void MakeMap()
    {
        map = std::vector<std::vector<PointType>>(
            max_y + 1, std::vector<PointType>(max_x + 1, PointType::UNKNOWN));
    }
    void MakeWalls()
    {
        for(uint32_t i; i < red_coords.size(); i++)
        {
            uint32_t x1 = red_coords[i].first;
            uint32_t y1 = red_coords[i].second;
            map[y1][x1] = PointType::VERTEX;

            uint32_t x2 = red_coords[0].first;
            uint32_t y2 = red_coords[0].second;
            if (i + 1 < red_coords.size())
            {
                x2 = red_coords[i+1].first;
                y2 = red_coords[i+1].second;
            }
            uint32_t x = 0;
            uint32_t y = 0;

            if(x2 > x1)
            {
                x = x1 + 1;
                y = y1;
                do
                {
                    map[y][x] = PointType::WALL_SOUTH;
                    x++;
                } while (x < x2);
            }
            else if(x2 < x1)
            {
                x = x1 - 1;
                y = y1;
                do
                {
                    map[y][x] = PointType::WALL_NORTH;
                    x--;
                } while (x > x2);                
            }
            else if(y2 > y1)
            {
                x = x1;
                y = y1 + 1;
                do
                {
                    map[y][x] = PointType::WALL_EAST;
                    y++;
                } while (y < y2);      

            }
            else if(y2 < y1)
            {
                x = x1;
                y = y1 - 1;
                do
                {
                    map[y][x] = PointType::WALL_WEST;
                    y--;
                } while (y > y2);
            }
        }
    }

    void MakeRectangles()
    {
        for(uint32_t i = 0; i < red_coords.size(); i++)
        {
            if(i % 50 == 0){std::cout << i << std::endl;}

            north_clear_dist = 0;
            north_fail_dist = max_distance_ever;
            east_clear_dist = 0;
            east_fail_dist = max_distance_ever;
            south_clear_dist = 0;
            south_fail_dist = max_distance_ever;
            west_clear_dist = 0;
            west_fail_dist = max_distance_ever;            

            uint32_t x1 = red_coords[i].first;
            uint32_t y1 = red_coords[i].second;

            uint32_t j = i + 1;
            while(j < red_coords.size())
            {
                uint32_t x2 = red_coords[j].first;
                uint32_t y2 = red_coords[j].second;

                RectDirection d = RectDirection::INVALID;
                uint32_t h = 0;
                uint32_t w = 0;
                uint32_t size = 0;
                if(x2 > x1 && y2 > y1)
                {
                    w = x2 - x1;
                    h = y2 - y1;
                    size = h * w;
                    if((east_fail_dist > w) && (north_fail_dist > h) && (size > max_size))
                    {
                        d = RectDirection::NORTH_EAST;
                        if(CheckNorthEast(x1, y1, x2, y2))
                        {
                            max_size = size;
                        }
                    }
                }
                else if(x2 > x1 && y2 < y1)
                {
                    w = x2 - x1;
                    h = y1 - y2;
                    size = h * w;
                    if((east_fail_dist > w) && (north_fail_dist > h) && (size > max_size))
                    {
                        d = RectDirection::SOUTH_EAST;
                        if(CheckSouthEast(x1, y1, x2, y2))
                        {
                            max_size = size;
                        }
                    }
                }
                else if(x2 < x1 && y2 < y1)
                {
                    w = x1 - x2;
                    h = y1 - y2;
                    size = h * w;
                    if((east_fail_dist > w) && (north_fail_dist > h) && (size > max_size))
                        {
                        d = RectDirection::SOUTH_WEST;
                        if(CheckSouthWest(x1, y1, x2, y2))
                        {
                            max_size = size;
                        }
                    }
                }
                else if(x2 < x1 && y2 > y1)
                {
                    w = x1 - x2;
                    h = y2 - y1;
                    size = h * w;
                    if((east_fail_dist > w) && (north_fail_dist > h) && (size > max_size))
                    {
                        d = RectDirection::NORTH_WEST;
                        if(CheckNorthWest(x1, y1, x2, y2))
                        {
                            max_size = size;
                        }
                    }
                }
                else
                {
                    // Same Row, skip
                }

                j++;
            }
        }
    }

    bool CheckBottomPoint(uint32_t x, uint32_t y, bool positive)
    {
        uint32_t straight = 1;
        if(!positive){straight = -1;}

        if(map[y][x] == PointType::VERTEX)
        {
            if( // Wall Comes in from outside
                (map[y][x+1] == PointType::WALL_SOUTH
                    || map[y][x+1] == PointType::VERTEX) &&
                (map[y-1][x] == PointType::WALL_EAST
                    || map[y-1][x] == PointType::VERTEX)
            ){} // Good
            else if( // Wall turns outside
                (map[y][x-1] == PointType::WALL_SOUTH
                    || map[y][x+1] == PointType::VERTEX) &&
                (map[y-1][x] == PointType::WALL_WEST
                    || map[y-1][x] == PointType::VERTEX)
            ){} // Good
            else if( // Wall continues straight
                (map[y][x+straight] == PointType::WALL_SOUTH
                    || map[y][x+straight] == PointType::VERTEX) &&
                (map[y+1][x] == PointType::UNKNOWN
                    && map[y-1][x] == PointType::UNKNOWN)
            ){} // Good
            else {return false;}
        }
        else if(map[y][x] == PointType::WALL_SOUTH){}// good
        else if(map[y][x] == PointType::UNKNOWN){}// good
        else if(map[y][x] == PointType::INSIDE){}// good
        else{return false;}

        return true;       
    }
    bool CheckTopPoint(uint32_t x, uint32_t y, bool positive)
    {
        uint32_t straight = 1;
        if(!positive){straight = -1;}

        if(map[y][x] == PointType::VERTEX)
        {
            if( // Wall Comes in from outside
                (map[y][x+1] == PointType::WALL_NORTH
                    || map[y][x+1] == PointType::VERTEX) &&
                (map[y-1][x] == PointType::WALL_EAST
                    || map[y-1][x] == PointType::VERTEX)
            ){} // Good
            else if( // Wall turns outside
                (map[y][x-1] == PointType::WALL_NORTH
                    || map[y][x+1] == PointType::VERTEX) &&
                (map[y-1][x] == PointType::WALL_WEST
                    || map[y-1][x] == PointType::VERTEX)
            ){} // Good
            else if( // Wall continues straight
                (map[y][x+straight] == PointType::WALL_NORTH
                    || map[y][x+straight] == PointType::VERTEX) &&
                (map[y+1][x] == PointType::UNKNOWN
                    && map[y-1][x] == PointType::UNKNOWN)
            ){} // Good
            else {return false;}
        }
        else if(map[y][x] == PointType::WALL_NORTH){}// good
        else if(map[y][x] == PointType::UNKNOWN){}// good
        else if(map[y][x] == PointType::INSIDE){}// good
        else{return false;}

        return true;       
    }
    bool CheckRightPoint(uint32_t x, uint32_t y, bool positive)
    {
        uint32_t straight = 1;
        if(!positive){straight = -1;}

        if(map[y][x] == PointType::VERTEX)
        {
            if( // Wall Comes in from outside
                (map[y+1][x] == PointType::WALL_EAST
                    || map[y+1][x] == PointType::VERTEX) &&
                (map[y][x+1] == PointType::WALL_NORTH
                    || map[y][x+1] == PointType::VERTEX)
            ){} // Good
            else if( // Wall turns outside
                (map[y-1][x] == PointType::WALL_EAST
                    || map[y-1][x] == PointType::VERTEX) &&
                (map[y][x+1] == PointType::WALL_SOUTH
                    || map[y][x+1] == PointType::VERTEX)
            ){} // Good
            else if( // Wall continues straight
                (map[y+straight][x] == PointType::WALL_EAST
                    || map[y+straight][x] == PointType::VERTEX) &&
                (map[y][x+1] == PointType::UNKNOWN
                    && map[y][x-1] == PointType::UNKNOWN)
            ){} // Good
            else {return false;}
        }
        else if(map[y][x] == PointType::WALL_EAST){}// good
        else if(map[y][x] == PointType::UNKNOWN){}// good
        else if(map[y][x] == PointType::INSIDE){}// good
        else{return false;}
        return true;
    }
    bool CheckLeftPoint(uint32_t x, uint32_t y, bool positive)
    {
        uint32_t straight = 1;
        if(!positive){straight = -1;}

        if(map[y][x] == PointType::VERTEX)
        {
            if( // Wall Comes in from outside
                (map[y+1][x] == PointType::WALL_WEST
                    || map[y+1][x] == PointType::VERTEX) &&
                (map[y][x+1] == PointType::WALL_NORTH
                    || map[y][x+1] == PointType::VERTEX)
            ){} // Good
            else if( // Wall turns outside
                (map[y-1][x] == PointType::WALL_WEST
                    || map[y-1][x] == PointType::VERTEX) &&
                (map[y][x+1] == PointType::WALL_SOUTH
                    || map[y][x+1] == PointType::VERTEX)
            ){} // Good
            else if( // Wall continues straight
                (map[y+straight][x] == PointType::WALL_WEST
                    || map[y+straight][x] == PointType::VERTEX) &&
                (map[y][x+1] == PointType::UNKNOWN
                    && map[y][x-1] == PointType::UNKNOWN)
            ){} // Good
            else {return false;}
        }
        else if(map[y][x] == PointType::WALL_WEST){}// good
        else if(map[y][x] == PointType::UNKNOWN){}// good
        else if(map[y][x] == PointType::INSIDE){}// good
        else{return false;}
        return true;
    }

    bool CheckNorthEast(uint32_t x1, uint32_t y1, uint32_t x2, uint32_t y2)
    {
        // Bottom 
        if(map[y1][x1+1] != PointType::WALL_SOUTH 
            && map[y1][x1+1] != PointType::VERTEX
            && map[y1][x1+1] != PointType::UNKNOWN) {return false;}

        uint32_t x = x1 + 1;
        if(x < x1 + east_clear_dist) { x = x1 + east_clear_dist; }
        for(; x <= x2; x++)
        {
            if(!CheckBottomPoint(x, y1, true))
            {
                east_fail_dist = x - x1;
                return false;
            }
            east_clear_dist++;
        }

        // Left
        if(map[y1+1][x1] != PointType::WALL_WEST
            && map[y1+1][x1] != PointType::VERTEX
            && map[y1+1][x1] != PointType::UNKNOWN) {return false;}
        uint32_t y = y1 + 1;
        if(y < y1 + north_clear_dist){y = y1 + north_clear_dist;}
        for(; y <= y2; y++)
        {
            if(!CheckLeftPoint(x1, y, true))
            {
                north_fail_dist = y - y1;
                return false;
            }
            north_clear_dist++;
        }

        // Right
        if(map[y1+1][x2] != PointType::WALL_EAST 
            && map[y1+1][x2] != PointType::VERTEX
            && map[y1+1][x2] != PointType::UNKNOWN) {return false;}

        for(uint32_t y = y1 + 1; y <= y2; y++)
        {
            if(!CheckRightPoint(x2, y, true)){return false;}
        }

        // Top
        if(map[y2][x1+1] != PointType::WALL_NORTH
            && map[y2][x1+1] != PointType::VERTEX
            && map[y2][x1+1] != PointType::UNKNOWN) {return false;}
        for(uint32_t x = x1 + 1; x < x2; x++)
        {
            if(!CheckTopPoint(x, y2, true)){return false;}
        }

        return true;
    }
    bool CheckSouthEast(uint32_t x1, uint32_t y1, uint32_t x2, uint32_t y2)
    {
        // Top
        if(map[y1][x1+1] != PointType::WALL_NORTH 
            && map[y1][x1+1] != PointType::VERTEX
            && map[y1][x1+1] != PointType::UNKNOWN) {return false;}

        uint32_t x = x1 + 1;
        if(x < x1 + east_clear_dist) { x = x1 + east_clear_dist; }
        for(; x <= x2; x++)
        {
            if(!CheckTopPoint(x, y1, true))
            {
                east_fail_dist = x - x1;
                return false;
            }
            east_clear_dist++;
        }

        // Left
        if(map[y1-1][x1] != PointType::WALL_WEST
            && map[y1-1][x1] != PointType::VERTEX
            && map[y1-1][x1] != PointType::UNKNOWN) {return false;}
        
        uint32_t y = y1 - 1;
        if(y > y1 - south_clear_dist) {y = y1 - south_clear_dist;}
        for(; y >= y2; y--)
        {
            if(!CheckLeftPoint(x1, y, false))
            {
                south_fail_dist = y - y1;
                return false;
            }
            south_clear_dist++;
        }

        // Right
        if(map[y1-1][x2] != PointType::WALL_EAST 
            && map[y1-1][x2] != PointType::VERTEX
            && map[y1-1][x2] != PointType::UNKNOWN) {return false;}

        for(uint32_t y = y1 - 1; y >= y2; y--)
        {
            if(!CheckRightPoint(x2, y, false)){return false;}
        }

        // Bottom
        if(map[y2][x1+1] != PointType::WALL_SOUTH
            && map[y2][x1+1] != PointType::VERTEX
            && map[y2][x1+1] != PointType::UNKNOWN) {return false;}

        for(uint32_t x = x1 + 1; x <= x2; x++)
        {
            if(!CheckBottomPoint(x, y2, true)){return false;}
        }
        return true;
    }
    bool CheckSouthWest(uint32_t x1, uint32_t y1, uint32_t x2, uint32_t y2)
    {
        // Top
        if(map[y1][x1-1] != PointType::WALL_NORTH 
            && map[y1][x1-1] != PointType::VERTEX
            && map[y1][x1-1] != PointType::UNKNOWN) {return false;}

        uint32_t x = x1 - 1;
        if(x > x1 - west_clear_dist) { x = x1 - west_clear_dist;}
        for(; x >= x2; x--)
        {
            if(!CheckTopPoint(x, y1, false))
            {
                west_fail_dist = x - x1;
                return false;
            }
            west_clear_dist++;
        }

        // Right
        if(map[y1-1][x1] != PointType::WALL_EAST 
            && map[y1-1][x1] != PointType::VERTEX
            && map[y1-1][x1] != PointType::UNKNOWN) {return false;}
        
        uint32_t y = y1 - 1;
        if(y > y1 - south_clear_dist) {y = y1 - south_clear_dist;}
        for(; y >= y2; y--)
        {
            if(!CheckRightPoint(x1, y, false))
            {
                south_fail_dist = y - y1;
                return false;
            }
            south_clear_dist++;
        }

        // Left
        if(map[y1-1][x2] != PointType::WALL_WEST 
            && map[y1-1][x2] != PointType::VERTEX
            && map[y1-1][x2] != PointType::UNKNOWN) {return false;}

        for(uint32_t y = y1 - 1; y >= y2; y--)
        {
            if(!CheckLeftPoint(x2, y, false)){return false;}
        }

        // Bottom
        if(map[y2][x1-1] != PointType::WALL_SOUTH
            && map[y2][x1-1] != PointType::VERTEX
            && map[y2][x1-1] != PointType::UNKNOWN) {return false;}

        for(uint32_t x = x1 - 1; x >= x2; x--)
        {
            if(!CheckBottomPoint(x, y2, true)){return false;}
        }
        return true;
    }
    bool CheckNorthWest(uint32_t x1, uint32_t y1, uint32_t x2, uint32_t y2)
    {
        // Bottom
        if(map[y1][x1-1] != PointType::WALL_SOUTH 
            && map[y1][x1-1] != PointType::VERTEX
            && map[y1][x1-1] != PointType::UNKNOWN) {return false;}

        uint32_t x = x1 - 1;
        if(x > x1 - west_clear_dist) { x = x1 - west_clear_dist; }
        for(; x <= x2; x++)
        {
            if(!CheckBottomPoint(x, y1, true))
            {
                west_fail_dist = x - x1;
                return false;
            }
            west_clear_dist++;
        }
        // Right
        if(map[y1+1][x1] != PointType::WALL_EAST
            && map[y1+1][x1] != PointType::VERTEX
            && map[y1+1][x1] != PointType::UNKNOWN) {return false;}

        uint32_t y = y1 + 1;
        if(y < y1 + north_clear_dist){y = y1 + north_clear_dist;}
        for(;y < y2; y++)
        {
            if(!CheckRightPoint(x1, y, true))
            {
                north_fail_dist = y - y1;
                return false;
            }
            north_clear_dist++;
        }

        // Left
        if(map[y1+1][x2] != PointType::WALL_WEST 
            && map[y1+1][x2] != PointType::VERTEX
            && map[y1+1][x2] != PointType::UNKNOWN) {return false;}

        for(uint32_t y = y1 + 1; y <= y2; y++)
        {
            if(!CheckLeftPoint(x2, y, true)){return false;}
        }

        // Top
        if(map[y2][x1-1] != PointType::WALL_NORTH
            && map[y2][x1-1] != PointType::VERTEX
            && map[y2][x1-1] != PointType::UNKNOWN) {return false;}

        for(uint32_t x = x1 - 1; x >= x2; x--)
        {
            if(!CheckTopPoint(x, y2, false)){return false;}
        }

        return true;
    }
    
    void PrintMap()
    {
        std::cout << "Map:" << std::endl;
        for(auto row : map)
        {
            for(PointType p : row)
            {
                if(p == PointType::UNKNOWN) {std::cout << ".";}
                else if(p == PointType::VERTEX) {std::cout << "#";}
                else if(p == PointType::WALL) {std::cout << "X";}
                else if(p == PointType::INSIDE) {std::cout << "I";}
                else if(p == PointType::OUTSIDE) {std::cout << "O";}
                else if(p == PointType::RECTANGEL) {std::cout << "R";}
                else if(p == PointType::WALL_NORTH) {std::cout << "N";}
                else if(p == PointType::WALL_SOUTH) {std::cout << "S";}
                else if(p == PointType::WALL_EAST) {std::cout << "E";}
                else if(p == PointType::WALL_WEST) {std::cout << "W";}
                else {throw std::runtime_error("Unknown point type.");}              
            }
            std::cout << std::endl;
        }
    }

    std::vector<std::pair<uint32_t, uint32_t>> red_coords;
    uint32_t max_x = 0;
    uint32_t max_y = 0;
    //uint32_t max_size = 0;
    uint32_t max_size = 205915986;

    uint32_t max_distance_ever = 1000000;
    uint32_t north_clear_dist = 0;
    uint32_t north_fail_dist = max_distance_ever;
    uint32_t east_clear_dist = 0;
    uint32_t east_fail_dist = max_distance_ever;
    uint32_t south_clear_dist = 0;
    uint32_t south_fail_dist = max_distance_ever;
    uint32_t west_clear_dist = 0;
    uint32_t west_fail_dist = max_distance_ever;

    std::vector<std::vector<PointType> > map;
    //std::vector<uint8_t> map;
};

int main(int argc, char* argv[])
{
    bool test = true;
    test = false;

    std::string inputFile = "tinput";
    if(!test)
    {
        inputFile = "input";
    }

    Solution s(inputFile);
    //s.PrintCoords();
    s.Run();
    if(test)
    {
        s.PrintMap();
    }

    std::cout << s.max_size << std::endl;

    return 0;
}

// 205915986 - Too low