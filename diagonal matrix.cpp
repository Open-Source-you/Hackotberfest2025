#include<iostream>

using namespace std;
void getinput(int** arr, int r, int c)
{
	cout << " Enter the entries of matrix : " << endl;
	for (int i = 0; i < r; i++)
	{
		for (int j = 0; j < c; j++)
		{
			cin >> arr[i][j];
		}
	}
}
void displaymatrix(int** arr, int r, int c)
{
	cout << " Display of matrix : " << endl;
	for (int i = 0; i < r; i++)
	{
		for (int j = 0; j < c; j++)
		{
			cout << arr[i][j]<<" ";
		}
		cout << endl;
	}
}
void check(int** arr, int r, int c)
{
	int count = 0;
	for (int i = 0; i < r; i++)
	{
		for (int j = 0; j < c; j++)
		{
			if (i != j && arr[i][j] != 0)
			{
				count = 1;
			}
		}
	}
	if (count == 1)
	{
		cout << " Matrix is not diagonal matrix " << endl;
	}
	else
		cout << " Matrix is a diagonal matrix " << endl;
}
void deallocatearray(int** arr, int r, int c)
{
	for (int i = 0; i < c; i++)
	{
		delete[]arr[i];
	}
	delete[]arr;
	arr = NULL;
}
int main()
{
	int rows;
	cout << " Enter the no. of rows: " << endl;
	cin >> rows;
	int cols;
	cout << " Enter the no. of columns: " << endl;
	cin >> cols;

	while (rows != cols)
	{
		cout << " ERROR! Enter again :" << endl;
		cout << " Enter the no. of columns: " << endl;
		cin >> cols;
		cout << " Enter the no. of rows: " << endl;
		cin >> rows;
	}

	int** arr = new int* [cols];
	for (int i = 0; i < cols; i++)
	{
		arr[i] = new int[rows];
	}
	getinput(arr, rows, cols);
	displaymatrix(arr, rows, cols);
	check(arr, rows, cols);
	deallocatearray(arr, rows, cols);

	return 0;
}
