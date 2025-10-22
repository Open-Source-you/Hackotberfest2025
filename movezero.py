def move_zeros(nums: list[int]) -> list[int]:
    """
    Moves all zeros in the list to the end while keeping other elements in order.
    """
    last_non_zero = 0
    for i in range(len(nums)):
        if nums[i] != 0:
            nums[last_non_zero], nums[i] = nums[i], nums[last_non_zero]
            last_non_zero += 1
    return nums

if __name__ == "__main__":
    arr = [0, 1, 0, 3, 12]
    print("Before:", arr)
    print("After: ", move_zeros(arr))
 last_non_zero = 0isidjcjjj
    for i in range(len(nums)):
        if nums[i] != 0:
            nums[last_non_zero], nums[i] = nums[i], nums[last_non_zero]
            last_non_zero += 1
    return nums
