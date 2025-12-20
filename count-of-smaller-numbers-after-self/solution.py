```python
import collections

class Solution:
    """
    Problem: Count of Smaller Numbers After Self

    You are given an integer array `nums`. You need to return an array `counts`
    where `counts[i]` is the number of smaller elements to the right of `nums[i]`.

    Example:
    Input: nums = [5, 2, 6, 1]
    Output: [2, 1, 1, 0]

    Explanation:
    - For nums[0] = 5, there are two smaller elements to its right: 2 and 1.
    - For nums[1] = 2, there is one smaller element to its right: 1.
    - For nums[2] = 6, there is one smaller element to its right: 1.
    - For nums[3] = 1, there are zero smaller elements to its right.
    """

    def countSmaller(self, nums: list[int]) -> list[int]:
        """
        Calculates the count of smaller numbers after self for each element in the input array.

        This solution uses a modified Merge Sort approach. The key idea is to augment
        each number with its original index and, during the merge step, when an element
        from the left sub-array is placed, count how many elements from the right
        sub-array have already been placed (meaning they are smaller and were
        originally to its right).

        Args:
            nums: A list of integers.

        Returns:
            A list of integers, where `counts[i]` is the number of smaller elements
            to the right of `nums[i]`.
        """
        n = len(nums)
        if n == 0:
            return []
        
        # We need to preserve the original index of each number
        # to correctly update the `ans` array. So, we store (value, original_index) pairs.
        indexed_nums = []
        for i in range(n):
            indexed_nums.append((nums[i], i))
        
        # This array will store the final counts. It's initialized to zeros.
        # `ans[i]` will store the count for the number originally at `nums[i]`.
        ans = [0] * n
        
        # The modified merge_sort function.
        # It takes a list of (value, original_index) tuples.
        # It sorts this list based on values and, as a side effect, updates the `ans` array.
        # It returns the sorted list of (value, original_index) tuples.
        def merge_sort(arr: list[tuple[int, int]]) -> list[tuple[int, int]]:
            # Base case: if the sub-array has 0 or 1 element, it's already sorted.
            if len(arr) <= 1:
                return arr
            
            # Divide the array into two halves
            mid = len(arr) // 2
            left_half = merge_sort(arr[:mid])
            right_half = merge_sort(arr[mid:])
            
            # Merge step: Combine the sorted left and right halves.
            # This is where the counting happens.
            merged_arr = []
            i, j = 0, 0 # Pointers for left_half and right_half respectively.
            
            # Iterate through both halves until one is exhausted.
            while i < len(left_half) and j < len(right_half):
                val_l, idx_l = left_half[i]
                val_r, idx_r = right_half[j]
                
                # If the element from the left half is less than or equal to the
                # element from the right half:
                # This `val_l` is greater than or equal to `val_r`. However, more importantly,
                # all elements in the `right_half` that have been *processed so far* (indicated by `j`)
                # are smaller than `val_l`. Since `left_half` and `right_half` come from
                # disjoint parts of the original array (left indices vs. right indices),
                # these `j` elements from the right half are indeed to the right of `val_l`
                # in the original array.
                # So, we add `j` to the count for the current left element (`val_l`).
                if val_l <= val_r:
                    ans[idx_l] += j
                    merged_arr.append(left_half[i])
                    i += 1
                # If the element from the right half is smaller than the left half element:
                # We simply append it to the merged array. It doesn't contribute to
                # counts of elements in the left half *yet* (it contributes by incrementing `j`).
                else: # val_l > val_r
                    merged_arr.append(right_half[j])
                    j += 1
            
            # After one of the halves is exhausted, append the remaining elements.
            # For any remaining elements in the `left_half`, all `j` elements that
            # were processed from the `right_half` are smaller than them.
            # (Because `right_half` elements were smaller than or equal to `val_l` and
            # `left_half` is sorted, so subsequent `val_l` are even larger)
            while i < len(left_half):
                val_l, idx_l = left_half[i]
                ans[idx_l] += j # Add the total count of elements taken from right_half
                merged_arr.append(left_half[i])
                i += 1
            
            # Any remaining elements in the `right_half` don't have corresponding
            # elements in the `left_half` to count against in this merge step.
            # Their counts will be determined when they are part of a left_half
            # in a higher-level merge.
            while j < len(right_half):
                merged_arr.append(right_half[j])
                j += 1
            
            return merged_arr

        # Start the merge sort process with the initial indexed numbers.
        # The `ans` array will be populated during the recursive calls.
        merge_sort(indexed_nums)
        
        return ans

    """
    Time Complexity:
    The algorithm is a modified Merge Sort.
    - Splitting the array into halves takes O(log N) levels of recursion.
    - Each level of recursion involves merging sub-arrays. The total work done
      in merging across all sub-arrays at a single level is O(N), where N
      is the original length of the input array.
    - Therefore, the total time complexity is O(N log N).

    Space Complexity:
    - The `indexed_nums` list stores (value, index) pairs, taking O(N) space.
    - The `ans` array also takes O(N) space.
    - The `merge_sort` function uses O(N) auxiliary space for the `merged_arr`
      in each merge step (though this space is reused across calls).
    - The recursion stack depth is O(log N).
    - Thus, the total space complexity is O(N).
    """

# Test Cases
if __name__ == "__main__":
    solver = Solution()

    # Test Case 1: Example from problem description
    nums1 = [5, 2, 6, 1]
    expected1 = [2, 1, 1, 0]
    result1 = solver.countSmaller(nums1)
    print(f"Input: {nums1}")
    print(f"Output: {result1}")
    print(f"Expected: {expected1}")
    assert result1 == expected1, f"Test Case 1 Failed: Expected {expected1}, Got {result1}"
    print("-" * 30)

    # Test Case 2: Empty array
    nums2 = []
    expected2 = []
    result2 = solver.countSmaller(nums2)
    print(f"Input: {nums2}")
    print(f"Output: {result2}")
    print(f"Expected: {expected2}")
    assert result2 == expected2, f"Test Case 2 Failed: Expected {expected2}, Got {result2}"
    print("-" * 30)

    # Test Case 3: Single element array
    nums3 = [1]
    expected3 = [0]
    result3 = solver.countSmaller(nums3)
    print(f"Input: {nums3}")
    print(f"Output: {result3}")
    print(f"Expected: {expected3}")
    assert result3 == expected3, f"Test Case 3 Failed: Expected {expected3}, Got {result3}"
    print("-" * 30)

    # Test Case 4: Array with all elements sorted in ascending order
    nums4 = [1, 2, 3, 4]
    expected4 = [0, 0, 0, 0]
    result4 = solver.countSmaller(nums4)
    print(f"Input: {nums4}")
    print(f"Output: {result4}")
    print(f"Expected: {expected4}")
    assert result4 == expected4, f"Test Case 4 Failed: Expected {expected4}, Got {result4}"
    print("-" * 30)

    # Test Case 5: Array with all elements sorted in descending order
    nums5 = [4, 3, 2, 1]
    expected5 = [3, 2, 1, 0]
    result5 = solver.countSmaller(nums5)
    print(f"Input: {nums5}")
    print(f"Output: {result5}")
    print(f"Expected: {expected5}")
    assert result5 == expected5, f"Test Case 5 Failed: Expected {expected5}, Got {result5}"
    print("-" * 30)

    # Test Case 6: Array with duplicate elements
    nums6 = [2, 0, 1, 2]
    expected6 = [2, 0, 0, 0]
    result6 = solver.countSmaller(nums6)
    print(f"Input: {nums6}")
    print(f"Output: {result6}")
    print(f"Expected: {expected6}")
    assert result6 == expected6, f"Test Case 6 Failed: Expected {expected6}, Got {result6}"
    print("-" * 30)
    
    # Test Case 7: Larger array with mixed numbers
    nums7 = [8, 1, 9, 3, 4, 7, 2, 5, 6, 0]
    # Expected:
    # 8: [1,3,4,7,2,5,6,0] => 1,3,4,7,2,5,6,0 (8 elements)
    # 1: [0] => 0 (1 element)
    # 9: [3,4,7,2,5,6,0] => 3,4,7,2,5,6,0 (7 elements)
    # 3: [2,0] => 2,0 (2 elements)
    # 4: [2,0] => 2,0 (2 elements)
    # 7: [2,5,6,0] => 2,5,6,0 (4 elements)
    # 2: [0] => 0 (1 element)
    # 5: [0] => 0 (1 element)
    # 6: [0] => 0 (1 element)
    # 0: [] => 0 (0 elements)
    expected7 = [8, 1, 7, 2, 2, 4, 1, 1, 1, 0]
    result7 = solver.countSmaller(nums7)
    print(f"Input: {nums7}")
    print(f"Output: {result7}")
    print(f"Expected: {expected7}")
    assert result7 == expected7, f"Test Case 7 Failed: Expected {expected7}, Got {result7}"
    print("-" * 30)

    print("All test cases passed!")
```