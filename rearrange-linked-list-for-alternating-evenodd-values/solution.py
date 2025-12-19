The problem asks us to rearrange a singly linked list such that its nodes alternate between even and odd values. The relative order of nodes within their original even or odd group must be preserved. If one type of value (even or odd) runs out, the remaining nodes of the other type should be appended to the end of the list. The rearrangement should prioritize starting with an odd node if available, then an even node, then odd, then even, and so on. If no odd nodes are available initially, it should start with an even node.

## Problem Description

Given the `head` of a singly linked list, rearrange the list such that its nodes alternate between even and odd values.

**Constraints:**
1.  The relative order of the original even values should be maintained.
2.  The relative order of the original odd values should be maintained.
3.  The alternating pattern should be `Odd -> Even -> Odd -> Even ...` if odd nodes are available to start.
4.  If no odd nodes are available, it should start with `Even -> Odd -> Even -> Odd ...` (though if no odds, it will just be `Even -> Even ...`).
5.  If one type of node is exhausted, the remaining nodes of the other type should be appended.

**Example 1:**
Input: `1 -> 2 -> 3 -> 4 -> 5`
- Odd nodes (maintaining relative order): `1 -> 3 -> 5`
- Even nodes (maintaining relative order): `2 -> 4`
Output: `1 -> 2 -> 3 -> 4 -> 5` (Odd, Even, Odd, Even, Odd)

**Example 2:**
Input: `2 -> 1 -> 4 -> 3 -> 6 -> 5`
- Odd nodes (maintaining relative order): `1 -> 3 -> 5`
- Even nodes (maintaining relative order): `2 -> 4 -> 6`
Output: `1 -> 2 -> 3 -> 4 -> 5 -> 6` (Odd, Even, Odd, Even, Odd, Even)

**Example 3:**
Input: `1 -> 3 -> 5` (All odd)
- Odd nodes: `1 -> 3 -> 5`
- Even nodes: (empty)
Output: `1 -> 3 -> 5`

**Example 4:**
Input: `2 -> 4 -> 6` (All even)
- Odd nodes: (empty)
- Even nodes: `2 -> 4 -> 6`
Output: `2 -> 4 -> 6`

## Solution Approach

The solution involves two main steps:

1.  **Separate the list into two sub-lists**: Traverse the original linked list. For each node, check if its value is odd or even. Create two new linked lists: one for all odd-valued nodes and one for all even-valued nodes. It's crucial to maintain the relative order of nodes within their respective groups and to detach each node from the original list as it's being added to a sub-list. This prevents cycles or unintended connections.

2.  **Merge the two sub-lists alternately**: Create a new merged linked list. Iterate through the odd and even sub-lists simultaneously. Append one node from the odd list, then one node from the even list, then one from the odd, and so on, to the merged list. This ensures the `Odd -> Even -> Odd -> Even` pattern. If one sub-list becomes empty, simply append all remaining nodes from the other sub-list.

To simplify the construction of linked lists (both separated and merged), dummy nodes are used. A dummy node serves as a temporary head, making it easier to handle insertions at the beginning of a list without special `if head is None` checks. The final result is `dummy.next`.

## Python Code

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def rearrangeList(self, head: ListNode) -> ListNode:
        """
        Rearranges a singly linked list to alternate between odd and even values.
        The relative order of original odd nodes is maintained, and similarly for even nodes.
        The rearranged list prioritizes starting with an odd node if available,
        then an even node, and so on. If one type of node runs out, the
        remaining nodes of the other type are appended.
        """
        
        # Edge case: empty list or list with a single node
        # No rearrangement needed, return as is.
        if not head or not head.next:
            return head

        # Step 1: Separate the original list into two sub-lists: one for odd values, one for even values.
        # We use dummy nodes to simplify list construction, avoiding special handling for the first node.
        odd_dummy = ListNode(0)
        even_dummy = ListNode(0)
        
        # Pointers to the current tails of the odd and even lists.
        # These pointers will be used to append new nodes.
        odd_ptr = odd_dummy
        even_ptr = even_dummy
        
        current = head
        while current:
            # Store the next node from the original list before modifying 'current.next'.
            # This is crucial to correctly traverse the original list while detaching nodes.
            next_node = current.next 
            
            # Detach the 'current' node from its original 'next' reference.
            # This ensures that our new sub-lists are independent and do not
            # accidentally form cycles or point to nodes in the other sub-list.
            current.next = None 
            
            if current.val % 2 != 0:  # Odd value
                odd_ptr.next = current
                odd_ptr = current
            else:  # Even value
                even_ptr.next = current
                even_ptr = current
            
            # Move to the next node in the original sequence
            current = next_node 
        
        # The actual heads of our separated odd and even lists are after their respective dummy nodes.
        odd_head = odd_dummy.next
        even_head = even_dummy.next

        # Step 2: Merge the odd and even sub-lists into a new alternating list.
        # We use another dummy node for the merged list to simplify appending.
        merged_dummy = ListNode(0)
        # Pointer to the current tail of the merged list.
        current_merged_tail = merged_dummy 
        
        ptr_odd = odd_head
        ptr_even = even_head
        
        # Continue merging as long as there are nodes remaining in either the odd or even list.
        while ptr_odd or ptr_even:
            # According to the problem, we prioritize appending an odd node first
            # to maintain the Odd -> Even -> Odd -> Even pattern.
            if ptr_odd:
                current_merged_tail.next = ptr_odd
                current_merged_tail = ptr_odd
                ptr_odd = ptr_odd.next
            
            # Then, append an even node if available.
            if ptr_even:
                current_merged_tail.next = ptr_even
                current_merged_tail = ptr_even
                ptr_even = ptr_even.next
                
        # The head of the completely rearranged list is after the 'merged_dummy' node.
        return merged_dummy.next

```

## Time and Space Complexity

### Time Complexity

*   **Separation Phase**: We iterate through the original linked list exactly once. Each node is processed in O(1) time (checking its value, updating pointers). If there are `N` nodes in the list, this phase takes O(N) time.
*   **Merging Phase**: We iterate through the two separated sub-lists (odd and even). In total, we process each of the `N` nodes exactly once again to build the merged list. This phase also takes O(N) time.

Therefore, the total time complexity is **O(N)**, where `N` is the number of nodes in the linked list.

### Space Complexity

*   **Auxiliary Space**: We use a few extra pointers (`odd_dummy`, `even_dummy`, `odd_ptr`, `even_ptr`, `current`, `next_node`, `merged_dummy`, `current_merged_tail`, `ptr_odd`, `ptr_even`). These are a constant number of variables, regardless of the input list size. We are rearranging existing nodes, not creating new ones (except for the dummy nodes, which are constant).

Therefore, the auxiliary space complexity is **O(1)**.

## Test Cases

To test the `rearrangeList` function, we'll need helper functions to create linked lists from Python lists and convert linked lists back to Python lists for easy verification.

```python
# Helper function to create a linked list from a list of values
def create_linked_list(arr):
    if not arr:
        return None
    head = ListNode(arr[0])
    current = head
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    return head

# Helper function to convert a linked list to a list of values
def linked_list_to_list(head):
    arr = []
    current = head
    while current:
        arr.append(current.val)
        current = current.next
    return arr

# Test cases
solution = Solution()

print("--- Test Cases ---")

# Test Case 1: Standard alternation, starts with odd
input_arr_1 = [1, 2, 3, 4, 5]
head_1 = create_linked_list(input_arr_1)
result_head_1 = solution.rearrangeList(head_1)
output_arr_1 = linked_list_to_list(result_head_1)
expected_arr_1 = [1, 2, 3, 4, 5]
print(f"Input: {input_arr_1}, Output: {output_arr_1}, Expected: {expected_arr_1} -> {'Passed' if output_arr_1 == expected_arr_1 else 'Failed'}")

# Test Case 2: Standard alternation, original starts with even but output starts with odd
input_arr_2 = [2, 1, 4, 3, 6, 5]
head_2 = create_linked_list(input_arr_2)
result_head_2 = solution.rearrangeList(head_2)
output_arr_2 = linked_list_to_list(result_head_2)
expected_arr_2 = [1, 2, 3, 4, 5, 6]
print(f"Input: {input_arr_2}, Output: {output_arr_2}, Expected: {expected_arr_2} -> {'Passed' if output_arr_2 == expected_arr_2 else 'Failed'}")

# Test Case 3: All odd numbers
input_arr_3 = [1, 3, 5, 7]
head_3 = create_linked_list(input_arr_3)
result_head_3 = solution.rearrangeList(head_3)
output_arr_3 = linked_list_to_list(result_head_3)
expected_arr_3 = [1, 3, 5, 7]
print(f"Input: {input_arr_3}, Output: {output_arr_3}, Expected: {expected_arr_3} -> {'Passed' if output_arr_3 == expected_arr_3 else 'Failed'}")

# Test Case 4: All even numbers
input_arr_4 = [2, 4, 6, 8]
head_4 = create_linked_list(input_arr_4)
result_head_4 = solution.rearrangeList(head_4)
output_arr_4 = linked_list_to_list(result_head_4)
expected_arr_4 = [2, 4, 6, 8]
print(f"Input: {input_arr_4}, Output: {output_arr_4}, Expected: {expected_arr_4} -> {'Passed' if output_arr_4 == expected_arr_4 else 'Failed'}")

# Test Case 5: Empty list
input_arr_5 = []
head_5 = create_linked_list(input_arr_5)
result_head_5 = solution.rearrangeList(head_5)
output_arr_5 = linked_list_to_list(result_head_5)
expected_arr_5 = []
print(f"Input: {input_arr_5}, Output: {output_arr_5}, Expected: {expected_arr_5} -> {'Passed' if output_arr_5 == expected_arr_5 else 'Failed'}")

# Test Case 6: Single node list (odd)
input_arr_6 = [7]
head_6 = create_linked_list(input_arr_6)
result_head_6 = solution.rearrangeList(head_6)
output_arr_6 = linked_list_to_list(result_head_6)
expected_arr_6 = [7]
print(f"Input: {input_arr_6}, Output: {output_arr_6}, Expected: {expected_arr_6} -> {'Passed' if output_arr_6 == expected_arr_6 else 'Failed'}")

# Test Case 7: Single node list (even)
input_arr_7 = [8]
head_7 = create_linked_list(input_arr_7)
result_head_7 = solution.rearrangeList(head_7)
output_arr_7 = linked_list_to_list(result_head_7)
expected_arr_7 = [8]
print(f"Input: {input_arr_7}, Output: {output_arr_7}, Expected: {expected_arr_7} -> {'Passed' if output_arr_7 == expected_arr_7 else 'Failed'}")

# Test Case 8: Mixed list, more odds than evens
input_arr_8 = [1, 2, 3, 4, 5, 6, 7]
head_8 = create_linked_list(input_arr_8)
result_head_8 = solution.rearrangeList(head_8)
output_arr_8 = linked_list_to_list(result_head_8)
expected_arr_8 = [1, 2, 3, 4, 5, 6, 7]
print(f"Input: {input_arr_8}, Output: {output_arr_8}, Expected: {expected_arr_8} -> {'Passed' if output_arr_8 == expected_arr_8 else 'Failed'}")

# Test Case 9: Mixed list, more evens than odds
input_arr_9 = [2, 1, 4, 3, 6, 8]
head_9 = create_linked_list(input_arr_9)
result_head_9 = solution.rearrangeList(head_9)
output_arr_9 = linked_list_to_list(result_head_9)
expected_arr_9 = [1, 2, 3, 4, 6, 8] # Odds: 1, 3. Evens: 2, 4, 6, 8. Merged: 1,2,3,4,6,8
print(f"Input: {input_arr_9}, Output: {output_arr_9}, Expected: {expected_arr_9} -> {'Passed' if output_arr_9 == expected_arr_9 else 'Failed'}")

# Test Case 10: Alternating list already, starting with odd
input_arr_10 = [1, 2, 3, 4, 5]
head_10 = create_linked_list(input_arr_10)
result_head_10 = solution.rearrangeList(head_10)
output_arr_10 = linked_list_to_list(result_head_10)
expected_arr_10 = [1, 2, 3, 4, 5]
print(f"Input: {input_arr_10}, Output: {output_arr_10}, Expected: {expected_arr_10} -> {'Passed' if output_arr_10 == expected_arr_10 else 'Failed'}")

# Test Case 11: Alternating list already, starting with even
input_arr_11 = [2, 1, 4, 3, 6]
head_11 = create_linked_list(input_arr_11)
result_head_11 = solution.rearrangeList(head_11)
output_arr_11 = linked_list_to_list(result_head_11)
expected_arr_11 = [1, 2, 3, 4, 6] # Odds: 1, 3. Evens: 2, 4, 6. Merged: 1,2,3,4,6
print(f"Input: {input_arr_11}, Output: {output_arr_11}, Expected: {expected_arr_11} -> {'Passed' if output_arr_11 == expected_arr_11 else 'Failed'}")

```