#include "test_frame.hpp"

int main()
{
    bool success;
    success = test_frame();
    if (success)
    {
        std::cout << "Test Frame conversion done succesfully"<< std::endl; 
    }
    else
    {
        std::cout<< "Test Frame conversion done unsuccessfully" << std::endl;
    }

}
