The "Largest Rectangle in Histogram" problem asks us to find the largest rectangle that can be formed within a histogram, where each bar has a width of 1.

## Problem Description

Given an array of integers `heights` representing the histogram's bar heights, where each bar has a width of 1, find the area of the largest rectangle in the histogram.

**Example:**

Input: `heights = [2,1,5,6,2,3]`
Output: `10`

Explanation: The largest rectangle is shown in the diagram, which has an area of `5 * 2 = 10`. The rectangle starts at index 2 (height 5) and extends to index 3 (height 6), but its height is limited by the minimum height within its width, which is 5. So, for the heights `[5, 6]`, the largest rectangle using both would be `5 * 2 = 10`.

## Python Solution

The most efficient way to solve this problem is by using a monotonic stack. The idea is to find, for each bar, the first smaller bar to its left and the first smaller bar to its right. These define the boundaries within which the current bar can act as the minimum height for a rectangle.

**Algorithm Steps:**

1.  **Initialize `max_area = 0`** and an empty `stack`. The stack will store indices of bars in increasing order of their heights.
2.  **Append a `0` to the `heights` array:** This acts as a sentinel to ensure all bars remaining in the stack are processed at the end.
3.  **Iterate through the extended `heights` array** (including the appended `0`):
    *   For each bar at index `i` with `current_height = heights[i]`:
    *   **While the stack is not empty AND `current_height` is less than the height of the bar at the top of the stack (`heights[stack[-1]]`):**
        *   This means the bar at `stack[-1]` can no longer extend to the right because `current_height` is shorter. We can now calculate the area for the popped bar.
        *   `h = heights[stack.pop()]` (The height of the bar being evaluated).
        *   `width`: The width of the rectangle for `h` is determined by its `right_boundary` (which is `i`, the current index) and its `left_boundary` (which is `stack[-1]` after popping, or `-1` if the stack becomes empty).
        *   `width = i - (stack[-1] if stack else -1) - 1`
        *   `max_area = max(max_area, h * width)`
    *   **Push `i` onto the stack:** This maintains the monotonic increasing property of heights for indices in the stack.
4.  **Return `max_area`**.

```python
class Solution:
    def largestRectangleArea(self, heights: list[int]) -> int:
        """
        Calculates the largest rectangle area in a histogram using a monotonic stack.

        Args:
            heights: A list of integers representing the heights of the histogram bars.

        Returns:
            The maximum area of a rectangle that can be formed in the histogram.
        """
        max_area = 0
        stack = []  # Stores indices of bars in increasing order of height

        # Append a 0 to the heights array to ensure all bars in the stack are processed.
        # This 0 acts as a sentinel, effectively making every remaining bar in the stack
        # 'taller' than the current bar, forcing them to be popped and their areas calculated.
        heights_extended = heights + [0]
        
        for i, current_height in enumerate(heights_extended):
            # While the stack is not empty AND the current bar is shorter than the bar
            # at the top of the stack:
            # This means the bar at stack.top() cannot extend further to the right than 'i'.
            # We can now calculate the area with stack.top() as the minimum height.
            while stack and current_height < heights_extended[stack[-1]]:
                # Pop the index of the bar that defines the height of the rectangle
                h = heights_extended[stack.pop()]
                
                # Calculate the width of the rectangle.
                # The right boundary is 'i' (the current index).
                # The left boundary is 'stack[-1]' (the index of the first bar to its left
                # that is shorter) or -1 if the stack is empty (meaning no shorter bar
                # to its left, so it extends to the beginning of the histogram).
                width = i - (stack[-1] if stack else -1) - 1
                
                max_area = max(max_area, h * width)
            
            # Push the current bar's index onto the stack.
            # The stack always maintains indices of bars in non-decreasing order of height.
            stack.append(i)
            
        return max_area

```

### Time and Space Complexity

*   **Time Complexity: O(N)**
    Each bar in the `heights` array is pushed onto the stack once and popped from the stack at most once. The operations inside the `while` loop (pop, calculate area) are constant time. Therefore, the total number of operations is proportional to `N`, where `N` is the number of bars in the histogram.

*   **Space Complexity: O(N)**
    In the worst-case scenario (e.g., a histogram with strictly increasing heights like `[1, 2, 3, 4, 5]`), all elements might be pushed onto the stack before any are popped (until the final `0` sentinel is processed). In such a case, the stack can store up to `N` indices.

### Test Cases

```python
import unittest

class TestLargestRectangleInHistogram(unittest.TestCase):

    def setUp(self):
        self.solution = Solution()

    def test_example_1(self):
        heights = [2, 1, 5, 6, 2, 3]
        expected_output = 10
        self.assertEqual(self.solution.largestRectangleArea(heights), expected_output)

    def test_example_2(self):
        heights = [2, 4]
        expected_output = 4
        self.assertEqual(self.solution.largestRectangleArea(heights), expected_output)
    
    def test_empty_histogram(self):
        heights = []
        expected_output = 0
        self.assertEqual(self.solution.largestRectangleArea(heights), expected_output)

    def test_single_bar(self):
        heights = [5]
        expected_output = 5
        self.assertEqual(self.solution.largestRectangleArea(heights), expected_output)

    def test_all_same_height(self):
        heights = [3, 3, 3, 3]
        expected_output = 12 # 3 * 4
        self.assertEqual(self.solution.largestRectangleArea(heights), expected_output)

    def test_increasing_heights(self):
        heights = [1, 2, 3, 4, 5]
        expected_output = 9 # (3*3 or 4*2 or 5*1) -> 3*3 (index 2 with width from 0 to 2)
        # More precisely, 1*5=5, 2*4=8, 3*3=9, 4*2=8, 5*1=5. Max is 9.
        self.assertEqual(self.solution.largestRectangleArea(heights), expected_output)

    def test_decreasing_heights(self):
        heights = [5, 4, 3, 2, 1]
        expected_output = 15 # 5*3 (index 0 with width from 0 to 2) -> actually 5*1=5, 4*2=8, 3*3=9, 2*4=8, 1*5=5. Max is 9.
        # Let's recheck this.
        # [5,4,3,2,1]
        # i=0, h=5, stack=[0]
        # i=1, h=4, 4<5, pop 0: h=5, w = 1-(-1)-1 = 1. area=5. max_area=5. stack=[]. push 1. stack=[1]
        # i=2, h=3, 3<4, pop 1: h=4, w = 2-(-1)-1 = 2. area=8. max_area=8. stack=[]. push 2. stack=[2]
        # i=3, h=2, 2<3, pop 2: h=3, w = 3-(-1)-1 = 3. area=9. max_area=9. stack=[]. push 3. stack=[3]
        # i=4, h=1, 1<2, pop 3: h=2, w = 4-(-1)-1 = 4. area=8. max_area=9. stack=[]. push 4. stack=[4]
        # i=5, h=0 (sentinel)
        #    0<1, pop 4: h=1, w = 5-(-1)-1 = 5. area=5. max_area=9. stack=[]
        expected_output = 9
        self.assertEqual(self.solution.largestRectangleArea(heights), expected_output)

    def test_complex_case(self):
        heights = [3, 1, 3, 2, 2]
        expected_output = 6 # e.g., using heights[0]=3, heights[2]=3, heights[3]=2, heights[4]=2 -> 2*3 = 6
        # Another one, 3*1=3, 1*5=5 (using heights[1] for all bars), 3*1=3, 2*2=4
        # Area = (index 2, height 3, width 1) = 3
        # Area = (index 0, height 3, width 1) = 3
        # Area = (index 1, height 1, width 5) = 5
        # Area = (index 3, height 2, width 2) = 4 (for [2,2])
        # Largest is 6.
        # Let's trace carefully for [3,1,3,2,2]
        # h_ext = [3,1,3,2,2,0]
        # i=0, h=3, stack=[0]
        # i=1, h=1, 1<3, pop 0: h=3, w=1-(-1)-1=1. area=3. max_area=3. stack=[]. push 1. stack=[1]
        # i=2, h=3, 3 not <1. push 2. stack=[1,2]
        # i=3, h=2, 2<3, pop 2: h=3, w=3-1-1=1. area=3. max_area=3. stack=[1].
        #    2 not <1. push 3. stack=[1,3]
        # i=4, h=2, 2 not <2. push 4. stack=[1,3,4]
        # i=5, h=0 (sentinel)
        #    0<2, pop 4: h=2, w=5-3-1=1. area=2. max_area=3. stack=[1,3]
        #    0<2, pop 3: h=2, w=5-1-1=3. area=6. max_area=6. stack=[1]
        #    0<1, pop 1: h=1, w=5-(-1)-1=5. area=5. max_area=6. stack=[]
        expected_output = 6
        self.assertEqual(self.solution.largestRectangleArea(heights), expected_output)

# To run the tests:
# if __name__ == '__main__':
#     unittest.main()
```