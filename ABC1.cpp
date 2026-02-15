#include <iostream>
#include <string>
#include <cctype>
using namespace std;

bool isHexNumber(const string& s) 
{
    if (s.empty()) return false;
    for (char c : s) 
    {
        if (!isxdigit(c)) return false;
    }
    return true;
}

int main() 
{
    string input;
    cout << "Введите строку для проверки: ";
    getline(cin, input);
    if (isHexNumber(input)) 
    {
        cout << "Корректная запись шестнадцатеричного числа.\n";
    } 
    else 
    {
        cout << "Некорректная запись.\n";
    }
    return 0;
}