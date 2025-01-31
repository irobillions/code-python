def firstMissingPositive(nums: list[int]) -> int:
    x = len(nums)
    for i in range(x):
        while 1 <= nums[i] <= x and nums[i] != nums[nums[i] - 1]:
            nums[nums[i] - 1], nums[i] = nums[i], nums[nums[i] - 1]

    for i in range(x):
        if nums[i] != i + 1:
            return i + 1

    return x + 1


if __name__ == '__main__':
    print(firstMissingPositive([3, 4, -1, 1]))
