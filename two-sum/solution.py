def two_sum(nums, target):
    """
    Given an array of integers nums and an integer target,
    return indices of the two numbers such that they add up to target.

    It is guaranteed that there will be exactly one solution,
    and you may not use the same element twice.

    Args:
        nums (list[int]): A list of integers.
        target (int): The target sum.

    Returns:
        list[int]: A list containing the indices of the two numbers that sum up to the target.

    Time Complexity:
        O(n) - We iterate through the list once.
               Dictionary lookups and insertions take O(1) on average.

    Space Complexity:
        O(n) - In the worst case, we might store all 'n' numbers in the hash map (dictionary)
               if no pair is found until the very end.
    """
    num_map = {}  # Dictionary to store (number: index) pairs

    for i, num in enumerate(nums):
        complement = target - num
        # Check if the complement exists in our map
        if complement in num_map:
            # If found, we have the two numbers.
            # The current number is at index 'i', and its complement
            # was previously seen at num_map[complement].
            return [num_map[complement], i]
        
        # If complement is not found, add the current number and its index to the map
        # for future lookups.
        num_map[num] = i

    # This part should ideally not be reached if exactly one solution is guaranteed.
    # However, for robustness in cases where a solution might not exist,
    # one could raise an error or return an empty list.
    return [] 

# Example Usage:
if __name__ == "__main__":
    # Example 1
    nums1 = [2, 7, 11, 15]
    target1 = 9
    result1 = two_sum(nums1, target1)
    print(f"Numbers: {nums1}, Target: {target1}")
    print(f"Indices: {result1}") # Expected: [0, 1] (because nums[0] + nums[1] == 2 + 7 == 9)

    print("-" * 30)

    # Example 2
    nums2 = [3, 2, 4]
    target2 = 6
    result2 = two_sum(nums2, target2)
    print(f"Numbers: {nums2}, Target: {target2}")
    print(f"Indices: {result2}") # Expected: [1, 2] (because nums[1] + nums[2] == 2 + 4 == 6)

    print("-" * 30)

    # Example 3
    nums3 = [3, 3]
    target3 = 6
    result3 = two_sum(nums3, target3)
    print(f"Numbers: {nums3}, Target: {target3}")
    print(f"Indices: {result3}") # Expected: [0, 1] (because nums[0] + nums[1] == 3 + 3 == 6)

    print("-" * 30)

    # Example 4: Larger numbers
    nums4 = [10, 20, 30, 40, 50]
    target4 = 70
    result4 = two_sum(nums4, target4)
    print(f"Numbers: {nums4}, Target: {target4}")
    print(f"Indices: {result4}") # Expected: [2, 3] (because nums[2] + nums[3] == 30 + 40 == 70)