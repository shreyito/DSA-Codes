```python
import heapq

class Solution:
    """
    Problem: Kth Largest Sum of Contiguous Subarrays

    Given an integer array 'nums' and an integer 'k',
    return the k-th largest sum of contiguous subarrays.

    A contiguous subarray is a sequence of elements that are adjacent in the array.
    The sum of a subarray is the total of all elements within that subarray.

    Example:
    nums = [10, -10, 20, -10], k = 1

    All contiguous subarrays and their sums:
    [10] -> 10
    [-10] -> -10
    [20] -> 20
    [-10] -> -10
    [10, -10] -> 0
    [-10, 20] -> 10
    [20, -10] -> 10
    [10, -10, 20] -> 20
    [-10, 20, -10] -> 0
    [10, -10, 20, -10] -> 10

    Sorted list of sums (descending): [20, 20, 10, 10, 10, 10, 0, 0, -10, -10]

    If k = 1, the 1st largest sum is 20.
    If k = 3, the 3rd largest sum is 10.

    Constraints (typical for this problem):
    - 1 <= nums.length <= 2000
    - -10^9 <= nums[i] <= 10^9
    - 1 <= k <= (nums.length * (nums.length + 1)) / 2
    """

    def kthLargestSum(self, nums: list[int], k: int) -> int:
        n = len(nums)

        # Step 1: Calculate prefix sums
        # prefix_sums[i] will store the sum of elements from nums[0] to nums[i-1].
        # prefix_sums[0] is initialized to 0 to handle subarrays starting from index 0.
        # This allows calculating sum(nums[i...j]) as prefix_sums[j+1] - prefix_sums[i] in O(1) time.
        prefix_sums = [0] * (n + 1)
        for i in range(n):
            prefix_sums[i+1] = prefix_sums[i] + nums[i]

        # Step 2: Use a min-heap to keep track of the k largest sums found so far.
        # A min-heap of size k ensures that its smallest element (root)
        # is the k-th largest sum encountered.
        min_heap = []

        # Step 3: Iterate through all possible contiguous subarrays.
        # 'i' represents the starting index of the subarray in the original 'nums' array.
        # 'j' represents the ending index of the subarray in the original 'nums' array.
        for i in range(n):
            for j in range(i, n):
                # Calculate the sum of the current subarray nums[i...j]
                # using the precomputed prefix sums.
                # sum(nums[i...j]) = prefix_sums[j+1] - prefix_sums[i]
                current_sum = prefix_sums[j+1] - prefix_sums[i]

                # If the heap has less than k elements, simply add the current sum.
                if len(min_heap) < k:
                    heapq.heappush(min_heap, current_sum)
                # If the heap is full (has k elements) AND the current sum is
                # larger than the smallest element in the heap (min_heap[0]),
                # then remove the smallest element and add the current sum.
                # This keeps the heap updated with the k largest sums seen so far.
                elif current_sum > min_heap[0]:
                    heapq.heapreplace(min_heap, current_sum)
        
        # After iterating through all possible subarrays, the min_heap will contain
        # the k largest sums. The smallest element in this min_heap (its root)
        # will be the k-th largest sum overall.
        return min_heap[0]

    """
    Complexity Analysis:

    Time Complexity: O(N^2 * log K)
    - Calculating prefix sums takes O(N) time.
    - There are N * (N + 1) / 2 = O(N^2) contiguous subarrays.
    - For each subarray sum, we perform at most one heap operation (push or replace).
      Heap operations (heappush, heapreplace) on a heap of size K take O(log K) time.
    - Therefore, the total time complexity is O(N) + O(N^2 * log K) = O(N^2 * log K).

    Space Complexity: O(N + K)
    - The `prefix_sums` array uses O(N) space.
    - The `min_heap` stores up to K elements, using O(K) space.
    - Therefore, the total space complexity is O(N + K).

    N is the length of the input array `nums`.
    K is the integer 'k' given in the problem.
    """


# Test Cases
if __name__ == "__main__":
    sol = Solution()

    # Test Case 1: Example from problem description
    nums1 = [10, -10, 20, -10]
    k1 = 1
    # Expected: 20 (largest sum is [10, -10, 20] or [20])
    # All sums: [10, -10, 20, -10, 0, 10, 10, 20, 0, 10]
    # Sorted desc: [20, 20, 10, 10, 10, 10, 0, 0, -10, -10]
    print(f"Test Case 1: nums={nums1}, k={k1} -> Expected: 20, Got: {sol.kthLargestSum(nums1, k1)}")
    assert sol.kthLargestSum(nums1, k1) == 20

    k1_b = 3
    # Expected: 10 (3rd largest sum)
    print(f"Test Case 1b: nums={nums1}, k={k1_b} -> Expected: 10, Got: {sol.kthLargestSum(nums1, k1_b)}")
    assert sol.kthLargestSum(nums1, k1_b) == 10

    k1_c = 8
    # Expected: 0 (8th largest sum)
    print(f"Test Case 1c: nums={nums1}, k={k1_c} -> Expected: 0, Got: {sol.kthLargestSum(nums1, k1_c)}")
    assert sol.kthLargestSum(nums1, k1_c) == 0


    # Test Case 2: All positive numbers
    nums2 = [1, 2, 3]
    k2 = 3
    # Subarrays & Sums: [1]->1, [2]->2, [3]->3, [1,2]->3, [2,3]->5, [1,2,3]->6
    # Sorted desc: [6, 5, 3, 3, 2, 1]
    # Expected: 3
    print(f"Test Case 2: nums={nums2}, k={k2} -> Expected: 3, Got: {sol.kthLargestSum(nums2, k2)}")
    assert sol.kthLargestSum(nums2, k2) == 3

    k2_b = 1
    # Expected: 6
    print(f"Test Case 2b: nums={nums2}, k={k2_b} -> Expected: 6, Got: {sol.kthLargestSum(nums2, k2_b)}")
    assert sol.kthLargestSum(nums2, k2_b) == 6

    k2_c = 6
    # Expected: 1 (smallest sum)
    print(f"Test Case 2c: nums={nums2}, k={k2_c} -> Expected: 1, Got: {sol.kthLargestSum(nums2, k2_c)}")
    assert sol.kthLargestSum(nums2, k2_c) == 1

    # Test Case 3: All negative numbers
    nums3 = [-1, -2, -3]
    k3 = 2
    # Subarrays & Sums: [-1]->-1, [-2]->-2, [-3]->-3, [-1,-2]->-3, [-2,-3]->-5, [-1,-2,-3]->-6
    # Sorted desc: [-1, -2, -3, -3, -5, -6]
    # Expected: -2
    print(f"Test Case 3: nums={nums3}, k={k3} -> Expected: -2, Got: {sol.kthLargestSum(nums3, k3)}")
    assert sol.kthLargestSum(nums3, k3) == -2

    k3_b = 1
    # Expected: -1
    print(f"Test Case 3b: nums={nums3}, k={k3_b} -> Expected: -1, Got: {sol.kthLargestSum(nums3, k3_b)}")
    assert sol.kthLargestSum(nums3, k3_b) == -1

    # Test Case 4: Single element array
    nums4 = [5]
    k4 = 1
    # Expected: 5
    print(f"Test Case 4: nums={nums4}, k={k4} -> Expected: 5, Got: {sol.kthLargestSum(nums4, k4)}")
    assert sol.kthLargestSum(nums4, k4) == 5

    # Test Case 5: Array with zeros
    nums5 = [0, 0, 0]
    k5 = 1
    # All sums are 0.
    # Expected: 0
    print(f"Test Case 5: nums={nums5}, k={k5} -> Expected: 0, Got: {sol.kthLargestSum(nums5, k5)}")
    assert sol.kthLargestSum(nums5, k5) == 0

    k5_b = 6 # Total subarrays: 3*(3+1)/2 = 6
    # Expected: 0
    print(f"Test Case 5b: nums={nums5}, k={k5_b} -> Expected: 0, Got: {sol.kthLargestSum(nums5, k5_b)}")
    assert sol.kthLargestSum(nums5, k5_b) == 0

    # Test Case 6: Mixed numbers with larger range
    nums6 = [-2, 5, -1, 3, -4]
    k6 = 5
    # Subarrays:
    # [-2]->-2, [5]->5, [-1]->-1, [3]->3, [-4]->-4
    # [-2,5]->3, [5,-1]->4, [-1,3]->2, [3,-4]->-1
    # [-2,5,-1]->2, [5,-1,3]->7, [-1,3,-4]->-2
    # [-2,5,-1,3]->5, [5,-1,3,-4]->3
    # [-2,5,-1,3,-4]->1
    # All sums: [-2, 5, -1, 3, -4, 3, 4, 2, -1, 2, 7, -2, 5, 3, 1]
    # Sorted desc: [7, 5, 5, 4, 3, 3, 3, 2, 2, 1, -1, -1, -2, -2, -4]
    # Expected: 3 (5th largest)
    print(f"Test Case 6: nums={nums6}, k={k6} -> Expected: 3, Got: {sol.kthLargestSum(nums6, k6)}")
    assert sol.kthLargestSum(nums6, k6) == 3

    print("\nAll test cases passed!")
```