def maxSubArray(nums: list[int]) -> int:
    max_xum = nums[0]
    current_sum = nums[0]

    for i in range(1, len(nums)):
        current_sum = max(nums[i], current_sum + nums[i])
        max_xum = max(current_sum, max_xum)

    return max_xum


if __name__ == '__main__':
    print(maxSubArray([-2, 1]))
