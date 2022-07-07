// MathApp.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream> // for outputing text and getting inputs
#include <string>
using namespace std;

int main()
{
    std::cout << "Let's do some math!\n";
    string opType;
    string a("add");
    string s("subtract");
    string m("multiply");
    string d("divide");

    std::cout << "Enter mathematical operation (add, subtract, multiply, divide): ";
    getline(cin, opType);
    std::cout << "Great! We will " << opType << " your numbers.\nPlease enter a number now...";
    int num1{}; //variables to store input number
    int num2{};
    std::cin >> num1; //get the user input
    std::cout << "Enter the next number...";
    std::cin >> num2;


    if ( !(opType.compare(a)) )
    {
        cout << "Adding...\n" << num1 << "+" << num2 << "=" << num1 + num2 << "\n";
    }
    else if (!(opType.compare(s)))
    {
        cout << "Subtracting...\n" << num1 << "-" << num2 << "=" << num1 - num2 << "\n";
    }
    else if (!(opType.compare(m)))
    {
        cout << "Multiplying...\n" << num1 << "*" << num2 << "=" << num1 * num2 << "\n";
    }
    else if (!(opType.compare(d)))
    {
        cout << "Dividing...\n" << num1 << "/" << num2 << "=" << num1 / num2 << "\n";
    }
    else
    {
        cout << "No such operation available..." << "\n";
    }
    return 0;
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
