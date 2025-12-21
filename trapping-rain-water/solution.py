```python
class Solution:
    def trap(self, height: list[int]) -> int:
        """
        Problem Description:
        Given n non-negative integers representing an elevation map where the width of each bar is 1,
        compute how much water it can trap after raining.

        An elevation map is represented by an array `height`. Each element `height[i]` represents
        the height of the i-th bar. We need to calculate the total amount of water that can be
        trapped between the bars.

        Example 1:
        Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
        Output: 6
        Explanation: The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1].
                     The blue sections represent the trapped rain water.

        Example 2:
        Input: height = [4,2,0,3,2,5]
        Output: 9
        Explanation: Here, 9 units of rain water are trapped.

        Constraints:
        n == height.length
        1 <= n <= 2 * 10^4
        0 <= height[i] <= 10^5

        Solution Approach: Two Pointers
        This approach uses two pointers, one starting from the left and one from the right,
        to efficiently calculate the trapped water. The key insight is that the amount of
        water trapped at any position `i` is determined by the minimum of the maximum height
        to its left and the maximum height to its right, minus its own height:
        `water[i] = min(max_left[i], max_right[i]) - height[i]`.

        With two pointers, `left` and `right`, and two variables `left_max` and `right_max`
        to keep track of the maximum heights encountered *so far* from their respective sides,
        we can calculate the water without explicitly building `max_left` and `max_right` arrays.

        When `height[left] < height[right]`:
        We know that the water trapped at `height[left]` (if any) is limited by `left_max`
        because there is *at least one* bar on the right side (`height[right]`) that is
        taller than `height[left]`. This means the right boundary for `height[left]` is
        guaranteed to be at least `height[right]` (and thus greater than `height[left]`).
        So, we can confidently calculate `left_max - height[left]`.

        When `height[right] <= height[left]`:
        Symmetrically, water trapped at `height[right]` is limited by `right_max` because
        there is *at least one* bar on the left side (`height[left]`) that is taller than
        or equal to `height[right]`. We calculate `right_max - height[right]`.
        """
        n = len(height)
        
        # If there are 2 or fewer bars, no water can be trapped.
        # This also correctly handles an empty array (n=0).
        if n <= 2:
            return 0

        left = 0             # Pointer starting from the left end
        right = n - 1        # Pointer starting from the right end
        
        left_max = 0         # Maximum height encountered from the left side so far
        right_max = 0        # Maximum height encountered from the right side so far
        
        total_water = 0      # Accumulator for the total trapped water

        # The loop continues as long as the left pointer is to the left of the right pointer.
        while left < right:
            # If the current left bar is shorter than the current right bar,
            # we focus on processing the left side.
            if height[left] < height[right]:
                # Update `left_max` if `height[left]` is a new highest bar on the left.
                if height[left] >= left_max:
                    left_max = height[left]
                else:
                    # If `height[left]` is smaller than `left_max`, it means `height[left]`
                    # can trap water. The water level is determined by `left_max`.
                    # We are sure `height[right]` (and thus `right_max`) is tall enough
                    # to form the right boundary for the water trapped at `height[left]`.
                    total_water += left_max - height[left]
                
                # Move the left pointer one step to the right.
                left += 1
            else:
                # If the current right bar is shorter than or equal to the current left bar,
                # we focus on processing the right side. This logic is symmetrical.
                # Update `right_max` if `height[right]` is a new highest bar on the right.
                if height[right] >= right_max:
                    right_max = height[right]
                else:
                    # If `height[right]` is smaller than `right_max`, it means `height[right]`
                    # can trap water. The water level is determined by `right_max`.
                    # We are sure `height[left]` (and thus `left_max`) is tall enough
                    # to form the left boundary for the water trapped at `height[right]`.
                    total_water += right_max - height[right]
                
                # Move the right pointer one step to the left.
                right -= 1

        return total_water

# Time Complexity: O(n)
# The two pointers `left` and `right` traverse the array from opposite ends
# and meet in the middle. Each element of the `height` array is visited and
# processed at most once. Therefore, the time complexity is linear with respect
# to the number of bars `n`.

# Space Complexity: O(1)
# The solution uses a constant amount of extra space, regardless of the input
# array size. We only maintain a few variables (`left`, `right`, `left_max`,
# `right_max`, `total_water`). No additional data structures that scale with `n`
# are created.

# Test Cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        ([0,1,0,2,1,0,1,3,2,1,2,1], 6, "Example 1 from description"),
        ([4,2,0,3,2,5], 9, "Example 2 from description"),
        ([0,0,0,0,0], 0, "All zeros, no water"),
        ([5,4,3,2,1], 0, "Monotonically decreasing, no water"),
        ([1,2,3,4,5], 0, "Monotonically increasing, no water"),
        ([5,1,5], 4, "Simple V-shape"),
        ([3,0,1,2,0,4], 10, "Complex case with multiple pits"),
        ([2,1,0,2], 1, "Pit at the beginning"),
        ([1,2,3], 0, "Small array, no water trapped"),
        ([1], 0, "Single bar, no water"),
        ([], 0, "Empty array, no water"),
        ([2,0,2], 2, "Simple pit between two bars"),
        ([4,2,3], 1, "Small pit between bars"),
        ([5,5,1,7,1,1,5], 14, "Multiple pits and flat tops"),
        ([6,4,2,0,3,2,0,3,1,4,5,3,2,7,5,3,0,1,2,1], 35, "Longer complex case")
    ]

    print("Running Trapping Rain Water tests...\n")
    for height, expected_output, description in test_cases:
        actual_output = solution.trap(height)
        print(f"Test Case: {description}")
        print(f"Input: {height}")
        print(f"Expected Output: {expected_output}")
        print(f"Actual Output: {actual_output}")
        assert actual_output == expected_output, \
            f"Test '{description}' FAILED! Expected {expected_output}, got {actual_output}"
        print("Status: PASSED\n" + "-"*30 + "\n")

    print("All test cases passed!")
```