#include <iostream>
using namespace std;

int adder(int x, int y) {
	return x + y;
}


int main() {
	int a, b;
	cout << "첫번째 수 입력 : ";
	cin >> a;
	cout << "두번째 수 입력 : ";
	cin >> b;

	cout << adder(a, b);
}