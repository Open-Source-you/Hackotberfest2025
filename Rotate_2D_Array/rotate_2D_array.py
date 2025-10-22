def rotate_array(arr: list[list[int|str]]) -> list[list[int|str]]:
    new_arr = []
    for j in range(len(arr[0])):
        new_row = []

        for i in range(len(arr)):
            new_row.append(arr[i][j])

        new_arr.append(new_row)

    return new_arr

# Driver code
def main():
    arr = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(rotate_array(arr))

if __name__ == "__main__":
    main()