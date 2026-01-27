# Problem Description:
# You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.
#
# Return the fewest number of coins that you need to make up that amount. If that amount cannot be made up by any combination of the coins, return -1.
#
# You may assume that you have an infinite number of each kind of coin.
#
# Example 1:
# Input: coins = [1, 2, 5], amount = 11 
# Output: 3
# Explanation: 11 = 5 + 5 + 1
#
# Example 2:
# Input: coins = [2], amount = 3
# Output: -1
#
# Example 3:
# Input: coins = [1], amount = 0
# Output: 0
#

class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        """
        Calculates the fewest number of coins needed to make up a given amount.

        This function uses dynamic programming to solve the coin change problem.
        It builds up a table `dp` where `dp[i]` stores the minimum number of coins
        required to form the amount `i`.

        Args:
            coins: A list of integers representing coin denominations. Each coin
                   denomination is positive.
            amount: An integer representing the total amount of money to be made.
                    It can be non-negative.

        Returns:
            The fewest number of coins needed to make up the amount.
            Returns -1 if the amount cannot be made up by any combination of the coins.
        """
        # Initialize dp array: dp[i] will store the minimum number of coins needed
        # to make up amount i.
        # We initialize all values to float('inf') to represent an unreachable state,
        # or an amount that cannot be formed.
        # The array size is `amount + 1` to cover amounts from 0 to `amount`.
        dp = [float('inf')] * (amount + 1)

        # Base case: 0 coins are needed to make up an amount of 0.
        dp[0] = 0

        # Iterate through each possible amount from 1 up to the target amount.
        # For each amount `i`, we try to find the minimum coins to form it.
        for i in range(1, amount + 1):
            # For each amount `i`, iterate through all available coin denominations.
            # We consider using each coin to reach the current amount `i`.
            for coin in coins:
                # If the current coin denomination `coin` is less than or equal to
                # the current amount `i`, then we can potentially use this coin.
                if i - coin >= 0:
                    # Update dp[i] with the minimum of its current value
                    # and (1 + dp[i - coin]).
                    # '1' represents using the current `coin`.
                    # `dp[i - coin]` represents the minimum coins needed for the
                    # remaining amount after using `coin`.
                    dp[i] = min(dp[i], 1 + dp[i - coin])
        
        # After filling the dp table, dp[amount] will contain the minimum number of coins
        # for the target amount.
        # If dp[amount] is still float('inf'), it means the amount cannot be made up
        # by any combination of the given coins. In this case, we return -1 as per problem statement.
        return dp[amount] if dp[amount] != float('inf') else -1

# Time and Space Complexity Analysis:
#
# Time Complexity: O(amount * N)
#   - We have an outer loop that iterates `amount` times (from 1 to `amount`).
#   - Inside this loop, we have an inner loop that iterates `N` times, where `N` is the number of coin denominations (`len(coins)`).
#   - Therefore, the total time complexity is proportional to `amount * N`.
#
# Space Complexity: O(amount)
#   - We use a dynamic programming array `dp` of size `amount + 1` to store intermediate results.
#   - The space required grows linearly with the target `amount`.

# Example Usage and Test Cases:
if __name__ == "__main__":
    solution = Solution()

    # Test Case 1: Standard case
    coins1 = [1, 2, 5]
    amount1 = 11
    expected1 = 3 # Explanation: 11 = 5 + 5 + 1
    result1 = solution.coinChange(coins1, amount1)
    print(f"Coins: {coins1}, Amount: {amount1}")
    print(f"Expected: {expected1}, Got: {result1}")
    assert result1 == expected1, f"Test Case 1 Failed: Expected {expected1}, Got {result1}"
    print("-" * 30)

    # Test Case 2: Amount cannot be made
    coins2 = [2]
    amount2 = 3
    expected2 = -1
    result2 = solution.coinChange(coins2, amount2)
    print(f"Coins: {coins2}, Amount: {amount2}")
    print(f"Expected: {expected2}, Got: {result2}")
    assert result2 == expected2, f"Test Case 2 Failed: Expected {expected2}, Got {result2}"
    print("-" * 30)

    # Test Case 3: Amount is 0 (base case)
    coins3 = [1]
    amount3 = 0
    expected3 = 0
    result3 = solution.coinChange(coins3, amount3)
    print(f"Coins: {coins3}, Amount: {amount3}")
    print(f"Expected: {expected3}, Got: {result3}")
    assert result3 == expected3, f"Test Case 3 Failed: Expected {expected3}, Got {result3}"
    print("-" * 30)

    # Test Case 4: Larger amount and more coins, optimal path
    coins4 = [1, 3, 4, 5]
    amount4 = 7
    expected4 = 2 # Explanation: 7 = 3 + 4
    result4 = solution.coinChange(coins4, amount4)
    print(f"Coins: {coins4}, Amount: {amount4}")
    print(f"Expected: {expected4}, Got: {result4}")
    assert result4 == expected4, f"Test Case 4 Failed: Expected {expected4}, Got {result4}"
    print("-" * 30)

    # Test Case 5: Only one coin type, exact match
    coins5 = [10]
    amount5 = 30
    expected5 = 3
    result5 = solution.coinChange(coins5, amount5)
    print(f"Coins: {coins5}, Amount: {amount5}")
    print(f"Expected: {expected5}, Got: {result5}")
    assert result5 == expected5, f"Test Case 5 Failed: Expected {expected5}, Got {result5}"
    print("-" * 30)

    # Test Case 6: Only one coin type, cannot make
    coins6 = [10]
    amount6 = 27
    expected6 = -1
    result6 = solution.coinChange(coins6, amount6)
    print(f"Coins: {coins6}, Amount: {amount6}")
    print(f"Expected: {expected6}, Got: {result6}")
    assert result6 == expected6, f"Test Case 6 Failed: Expected {expected6}, Got {result6}"
    print("-" * 30)

    # Test Case 7: Coins include larger values, amount is small, cannot make
    coins7 = [100, 200, 500]
    amount7 = 150
    expected7 = -1
    result7 = solution.coinChange(coins7, amount7)
    print(f"Coins: {coins7}, Amount: {amount7}")
    print(f"Expected: {expected7}, Got: {result7}")
    assert result7 == expected7, f"Test Case 7 Failed: Expected {expected7}, Got {result7}"
    print("-" * 30)
    
    # Test Case 8: Coins include 1, making any amount possible
    coins8 = [1, 7, 10]
    amount8 = 15
    expected8 = 3 # 10 + 1 + 1 + 1 + 1 + 1 (5 coins) or 7 + 7 + 1 (3 coins) or 10 + 5 (2 coins, if 5 was available. Here it is not, so 7+7+1)
    result8 = solution.coinChange(coins8, amount8)
    print(f"Coins: {coins8}, Amount: {amount8}")
    print(f"Expected: {expected8}, Got: {result8}")
    assert result8 == expected8, f"Test Case 8 Failed: Expected {expected8}, Got {result8}"
    print("-" * 30)


    print("All test cases passed successfully!")
