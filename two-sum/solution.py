def two_sum(nums: list[int], target: int) -> list[int]:
    """
    Given an array of integers nums and an integer target,
    return indices of the two numbers such that they add up to target.

    Assumptions:
    - Each input will have exactly one solution.
    - You may not use the same element twice.

    Args:
        nums (list[int]): A list of integers.
        target (int): The target sum.

    Returns:
        list[int]: A list containing the indices of the two numbers that sum up to target.

    Time Complexity:
    O(n) - We iterate through the list of numbers once. Dictionary (hash map)
    lookups and insertions take O(1) time on average. In the worst case, if
    there are many hash collisions, it could degrade to O(n) for dictionary
    operations, but this is rare with good hash functions.

    Space Complexity:
    O(n) - In the worst case, we might store all 'n' numbers and their indices
    in the hash map before finding the pair. Each entry in the hash map stores
    a number and its index.
    """
    # A dictionary to store numbers and their indices as we iterate through the list.
    # Key: number, Value: index
    num_map = {}

    for i, num in enumerate(nums):
        # Calculate the 'complement' needed to reach the target.
        complement = target - num

        # Check if the complement already exists in our map.
        # If it does, we've found the two numbers.
        if complement in num_map:
            # Return the index of the complement (stored in num_map) and the
            # current number's index.
            return [num_map[complement], i]
        
        # If the complement is not found, add the current number and its index
        # to the map for future lookups.
        num_map[num] = i
    
    # According to the problem statement, each input has exactly one solution,
    # so this line should technically not be reached.
    # However, it's good practice to consider what to return if no solution is found.
    # For this problem, we can assume a solution always exists.
    return [] # Or raise an error if no solution is guaranteed.

# Example Usage:
if __name__ == "__main__":
    # Example 1
    nums1 = [2, 7, 11, 15]
    target1 = 9
    result1 = two_sum(nums1, target1)
    print(f"Nums: {nums1}, Target: {target1} -> Result: {result1}") # Expected: [0, 1] (because 2 + 7 = 9)

    # Example 2
    nums2 = [3, 2, 4]
    target2 = 6
    result2 = two_sum(nums2, target2)
    print(f"Nums: {nums2}, Target: {target2} -> Result: {result2}") # Expected: [1, 2] (because 2 + 4 = 6)

    # Example 3
    nums3 = [3, 3]
    target3 = 6
    result3 = two_sum(nums3, target3)
    print(f"Nums: {nums3}, Target: {target3} -> Result: {result3}") # Expected: [0, 1] (because 3 + 3 = 6)

    # Example 4 (numbers with negative values)
    nums4 = [-1, -2, -3, -4, -5]
    target4 = -8
    result4 = two_sum(nums4, target4)
    print(f"Nums: {nums4}, Target: {target4} -> Result: {result4}") # Expected: [2, 4] (because -3 + -5 = -8)

    # Example 5 (target is zero)
    nums5 = [1, 0, -1]
    target5 = 0
    result5 = two_sum(nums5, target5)
    print(f"Nums: {nums5}, Target: {target5} -> Result: {result5}") # Expected: [0, 2] (because 1 + -1 = 0)
<ctrl63>