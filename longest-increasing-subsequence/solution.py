```python
import bisect

def lengthOfLIS(nums: list[int]) -> int:
    """
    Calculates the length of the Longest Increasing Subsequence (LIS) in a given array.

    Problem Description:
    The Longest Increasing Subsequence problem is to find the length of the longest 
    subsequence of a given sequence such that all elements of the subsequence are 
    sorted in strictly increasing order.

    For example:
    Given nums = [10, 9, 2, 5, 3, 7, 101, 18]
    The LIS is [2, 3, 7, 18], and its length is 4.

    This solution uses an optimized dynamic programming approach with binary search,
    achieving O(n log n) time complexity.

    Algorithm Explanation:
    The core idea is to maintain a `tails` array. `tails[i]` stores the smallest
    ending element of an increasing subsequence of length `i+1`.

    1.  Initialize an empty list `tails`. This list will store the smallest ending
        elements for increasing subsequences of various lengths. Importantly, `tails`
        will always be sorted in increasing order.

    2.  Iterate through each number `num` in the input `nums` array:
        a.  Use `bisect_left(tails, num)` to find the index `idx` where `num` could be
            inserted into `tails` to maintain its sorted order.
            `bisect_left` returns an insertion point that comes before (to the left of)
            any existing entries of `num` in `tails`.

        b.  If `idx` is equal to the current length of `tails`:
            This means `num` is greater than all elements currently in `tails`.
            It implies we've found an increasing subsequence that is one element
            longer than any previous one. So, we append `num` to `tails`.
            Example: `tails = [2, 5]`, `num = 7`. `idx = 2`. `tails` becomes `[2, 5, 7]`.

        c.  Otherwise (if `idx < len(tails)`):
            This means `num` is not strictly greater than all elements in `tails`.
            `num` can potentially replace `tails[idx]`.
            We replace `tails[idx]` with `num`. The reasoning is: we found an
            increasing subsequence of length `idx + 1` that ends with a smaller number
            (`num`) than what we had previously (`tails[idx]`). A smaller ending element
            is always preferable because it provides more opportunities to extend the
            subsequence further with future numbers.
            Example: `tails = [2, 5]`, `num = 3`. `idx = 1`. `tails[1]` (which is 5) is
            replaced by 3. `tails` becomes `[2, 3]`. We still have an LIS of length 2,
            but `[2, 3]` is "better" than `[2, 5]` for future extensions.

    3.  After iterating through all numbers, the final length of the `tails` array
        will be the length of the Longest Increasing Subsequence. Each time we append
        to `tails`, we effectively extend the maximum length of an LIS found so far.

    Args:
        nums: A list of integers.

    Returns:
        The length of the Longest Increasing Subsequence.
    """
    if not nums:
        return 0

    tails = []  # tails[i] stores the smallest ending element of an increasing subsequence of length i+1

    for num in nums:
        # Find the insertion point for 'num' in 'tails'
        # This is essentially finding the smallest element in 'tails' that is >= 'num'
        idx = bisect.bisect_left(tails, num)

        if idx == len(tails):
            # If 'num' is greater than all elements in 'tails',
            # it extends the longest increasing subsequence found so far.
            tails.append(num)
        else:
            # If 'num' is not greater than all elements,
            # it replaces tails[idx]. This forms an increasing subsequence
            # of the same length (idx + 1) but ending with a smaller number,
            # which is more optimal for future extensions.
            tails[idx] = num

    # The length of 'tails' is the length of the LIS.
    return len(tails)


# --- Time and Space Complexity ---
# Time Complexity: O(n log n)
# - The algorithm iterates through each number in the input list `nums` once. This is O(n) operations.
# - Inside the loop, `bisect.bisect_left` performs a binary search on the `tails` list.
#   The `tails` list can grow up to a maximum size of `n` (in the worst case, if `nums` is strictly increasing).
#   A binary search on a list of size `k` takes O(log k) time. In our case, `k` can be up to `n`,
#   so each `bisect_left` operation takes O(log n) time.
# - Appending or updating an element in `tails` takes O(1) time (amortized for append, O(1) for direct update).
# - Therefore, the total time complexity is dominated by the `n` binary search operations, resulting in O(n log n).

# Space Complexity: O(n)
# - The `tails` list stores at most `n` elements (in the worst case, when `nums` itself is a strictly increasing sequence).
# - Thus, the space complexity is O(n) to store the `tails` list.


# --- Test Cases ---
if __name__ == "__main__":
    test_cases = [
        ([10, 9, 2, 5, 3, 7, 101, 18], 4),  # Example from problem description: LIS [2, 3, 7, 18]
        ([0, 1, 0, 3, 2, 3], 4),            # LIS [0, 1, 2, 3]
        ([7, 7, 7, 7, 7, 7, 7], 1),         # All same numbers, LIS is just one number
        ([], 0),                            # Empty list
        ([1], 1),                           # Single element
        ([1, 2, 3, 4, 5], 5),               # Already sorted
        ([5, 4, 3, 2, 1], 1),               # Strictly decreasing
        ([3, 1, 2, 4], 3),                  # LIS [1, 2, 4]
        ([1, 3, 6, 7, 9, 4, 10, 5, 6], 6),  # LIS [1, 3, 6, 7, 9, 10] or [1, 3, 4, 5, 6, 10] (length 6)
    ]

    print("--- Running Test Cases for Longest Increasing Subsequence ---")
    for i, (nums, expected) in enumerate(test_cases):
        result = lengthOfLIS(nums)
        print(f"\nTest Case {i+1}:")
        print(f"Input: {nums}")
        print(f"Expected LIS length: {expected}")
        print(f"Actual LIS length:   {result}")
        assert result == expected, f"Test Case {i+1} Failed: Expected {expected}, got {result}"
        print(f"Status: PASSED")

    print("\nAll test cases passed!")
```