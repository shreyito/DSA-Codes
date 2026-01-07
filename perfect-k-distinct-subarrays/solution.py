The "Perfect K-Distinct Subarrays" problem asks us to find subarrays that meet two specific criteria simultaneously: they must have a length of exactly `k`, and they must contain exactly `k` distinct elements. This implies that all elements within such a subarray must be unique.

This problem can be efficiently solved using the **sliding window technique**. We maintain a window of size `k` as it slides through the array. For each window, we track the frequency of its elements to determine the count of distinct elements.

### Problem Description

Given an integer array `nums` and an integer `k`, return the number of "perfect K-distinct subarrays". A subarray is considered "perfect K-distinct" if it satisfies both of the following conditions:

1.  Its length is exactly `k`.
2.  It contains exactly `k` distinct elements.

Effectively, we are counting subarrays of length `k` where all elements within that subarray are unique.

**Example:**
`nums = [1,2,1,2,3], k = 3`

Let's examine the subarrays of length 3:
*   `[1,2,1]` - Length 3, distinct elements: `{1, 2}` (count = 2). Not perfect (does not have 3 distinct elements).
*   `[2,1,2]` - Length 3, distinct elements: `{1, 2}` (count = 2). Not perfect.
*   `[1,2,3]` - Length 3, distinct elements: `{1, 2, 3}` (count = 3). Perfect!

The total count of perfect K-distinct subarrays is 1.

### Python Solution

```python
import collections

class Solution:
    def perfect_k_distinct_subarrays(self, nums: list[int], k: int) -> int:
        """
        Calculates the number of "perfect K-distinct subarrays" in a given array.
        A subarray is perfect K-distinct if it has a length of K and contains
        exactly K distinct elements (i.e., all elements are unique within the subarray).

        Args:
            nums: The input list of integers.
            k: The desired length and number of distinct elements for a perfect subarray.

        Returns:
            The total count of perfect K-distinct subarrays.
        """
        n = len(nums)
        
        # Edge cases:
        # If k is non-positive or k is greater than the array length,
        # it's impossible to form such subarrays.
        if k <= 0 or k > n:
            return 0

        perfect_subarray_count = 0
        
        # Frequency map (dictionary) to store counts of elements in the current window.
        # Using collections.defaultdict(int) simplifies handling new elements.
        freq_map = collections.defaultdict(int)
        
        left = 0  # Left pointer of the sliding window
        
        # Iterate with the right pointer to expand the window.
        for right in range(n):
            # Add the current element at the right pointer to the frequency map.
            freq_map[nums[right]] += 1
            
            # Check if the current window has reached the desired size 'k'.
            # The window size is calculated as (right - left + 1).
            if (right - left + 1) == k:
                # If the number of distinct elements in the window (len(freq_map))
                # is exactly 'k', it means all elements in this window are unique.
                if len(freq_map) == k:
                    perfect_subarray_count += 1
                
                # Now, shrink the window from the left side.
                # Decrement the count of the element at the left pointer.
                freq_map[nums[left]] -= 1
                
                # If the count of the leftmost element becomes zero after decrementing,
                # it means this element is no longer present in the window.
                # Remove it from the frequency map to accurately reflect the distinct elements count.
                if freq_map[nums[left]] == 0:
                    del freq_map[nums[left]]
                
                # Move the left pointer forward to slide the window.
                left += 1
                
        return perfect_subarray_count

```

### Time and Space Complexity

*   **Time Complexity: O(N)**
    The `right` pointer iterates through the `nums` array once, visiting each element. The `left` pointer also moves at most `N` times. Operations within the loop (adding/removing elements from `freq_map`, checking `len(freq_map)`) take `O(1)` on average for a hash map (dictionary). Therefore, the overall time complexity is linear with respect to the number of elements in `nums`.

*   **Space Complexity: O(k)**
    The `freq_map` stores the counts of distinct elements within the current sliding window. Since the window size is fixed at `k`, the `freq_map` will store at most `k` distinct elements. In the worst case, `k` could be equal to `N` (the length of `nums`), so the space complexity is `O(N)` in the worst case, but generally `O(k)`.

### Test Cases

```python
# Create an instance of the Solution class
solver = Solution()

# Test Case 1: Basic example
nums1 = [1,2,1,2,3]
k1 = 3
# Expected: 1 ([1,2,3] is the only perfect subarray)
print(f"Test Case 1: nums={nums1}, k={k1} -> Result: {solver.perfect_k_distinct_subarrays(nums1, k1)}")


# Test Case 2: No perfect subarrays (duplicates in all length-k windows)
nums2 = [1,1,1,1,1]
k2 = 3
# Expected: 0 (e.g., [1,1,1] has only 1 distinct element, not 3)
print(f"Test Case 2: nums={nums2}, k={k2} -> Result: {solver.perfect_k_distinct_subarrays(nums2, k2)}")


# Test Case 3: All elements are unique
nums3 = [1,2,3,4,5]
k3 = 3
# Expected: 3 ([1,2,3], [2,3,4], [3,4,5] are perfect subarrays)
print(f"Test Case 3: nums={nums3}, k={k3} -> Result: {solver.perfect_k_distinct_subarrays(nums3, k3)}")


# Test Case 4: k equals array length, all unique
nums4 = [1,2,3]
k4 = 3
# Expected: 1 ([1,2,3] is perfect)
print(f"Test Case 4: nums={nums4}, k={k4} -> Result: {solver.perfect_k_distinct_subarrays(nums4, k4)}")


# Test Case 5: k equals array length, not all unique
nums5 = [1,2,1]
k5 = 3
# Expected: 0
print(f"Test Case 5: nums={nums5}, k={k5} -> Result: {solver.perfect_k_distinct_subarrays(nums5, k5)}")


# Test Case 6: k is greater than array length
nums6 = [1,2]
k6 = 3
# Expected: 0 (handled by initial k > n check)
print(f"Test Case 6: nums={nums6}, k={k6} -> Result: {solver.perfect_k_distinct_subarrays(nums6, k6)}")


# Test Case 7: k = 1 (every single element forms a perfect subarray)
nums7 = [1,2,1,3]
k7 = 1
# Expected: 4 ([1], [2], [1], [3] are all perfect)
print(f"Test Case 7: nums={nums7}, k={k7} -> Result: {solver.perfect_k_distinct_subarrays(nums7, k7)}")


# Test Case 8: Empty array
nums8 = []
k8 = 2
# Expected: 0 (handled by initial k > n check, n=0)
print(f"Test Case 8: nums={nums8}, k={k8} -> Result: {solver.perfect_k_distinct_subarrays(nums8, k8)}")


# Test Case 9: k = 0
nums9 = [1,2,3]
k9 = 0
# Expected: 0 (handled by initial k <= 0 check)
print(f"Test Case 9: nums={nums9}, k={k9} -> Result: {solver.perfect_k_distinct_subarrays(nums9, k9)}")

# Test Case 10: Mixed elements, multiple perfect subarrays
nums10 = [1,5,1,2,3,4,5]
k10 = 3
# Expected: 3
# [1,5,1] -> distinct=2, not perfect
# [5,1,2] -> distinct=3, perfect! (count=1)
# [1,2,3] -> distinct=3, perfect! (count=2)
# [2,3,4] -> distinct=3, perfect! (count=3)
# [3,4,5] -> distinct=3, perfect! (count=4)
print(f"Test Case 10: nums={nums10}, k={k10} -> Result: {solver.perfect_k_distinct_subarrays(nums10, k10)}")
```