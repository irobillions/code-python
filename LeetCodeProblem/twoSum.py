def twoSum(nums: list[int], target: int) -> list[int]:
    index_list = []

    for i in range(len(nums)):
        val = target - nums[i]
        if val in nums:
            if val != nums[i]:
                index_list.extend([i, nums.index(val)])
                break
            else:
                if nums.count(val) == 2:
                    index_list.extend([t for t, x in enumerate(nums) if x == val])
                    break

    return index_list


def twoSum2(nums: list[int], target: int) -> list[int]:
    seen = {}

    for i, val in enumerate(nums):
        complement = target - val
        if complement in seen:
            return [seen[complement], i]
        seen[val] = i


if __name__ == '__main__':
    tab = [3, 3]
    target = 6
    print(twoSum2(tab, target))
