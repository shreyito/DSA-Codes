```python
# Problem Description:
# You are given the head of a singly linked list L: L0 → L1 → … → Ln - 1 → Ln.
# Reorder the list to be on the following form: L0 → Ln → L1 → Ln - 1 → L2 → Ln - 2 → …
# You must do this in-place without modifying the nodes' values.

# Example 1:
# Input: head = [1,2,3,4]
# Output: [1,4,2,3]

# Example 2:
# Input: head = [1,2,3,4,5]
# Output: [1,5,2,4,3]

# Constraints:
# The number of nodes in the list is in the range [1, 5 * 10^4].
# 1 <= Node.val <= 1000

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reorderList(self, head: ListNode) -> None:
        """
        Do not return anything, modify head in-place instead.
        
        Time Complexity: O(N)
            1. Finding the middle of the list takes O(N) time.
            2. Reversing the second half of the list takes O(N/2), which is O(N) time.
            3. Merging the two halves takes O(N/2), which is O(N) time.
            Overall, the time complexity is O(N).

        Space Complexity: O(1)
            The solution uses a few extra pointers but does not create new nodes or data structures
            that scale with the input size. All modifications are done in-place.
        """
        # Base case: If the list is empty or has only one node, no reordering is needed.
        if not head or not head.next:
            return

        # Step 1: Find the middle of the linked list
        # We use slow and fast pointers. 'slow' will eventually point to the last node
        # of the first half of the list. 'fast' starts one step ahead to ensure correct
        # splitting for both even and odd length lists.
        # Example: 1->2->3->4->5  => slow ends at 3. First half: 1->2->3, Second half: 4->5
        # Example: 1->2->3->4    => slow ends at 2. First half: 1->2, Second half: 3->4
        slow = head
        fast = head.next 
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        # At this point, 'slow' is the end of the first half.
        # 'slow.next' is the head of the second half.

        # Step 2: Split the list into two halves
        # head1 will be the first half, starting from the original head.
        # head2 will be the second half, starting from 'slow.next'.
        head1 = head         
        head2 = slow.next    
        slow.next = None     # Cut the link to separate the two halves.
                             # This effectively makes the first half a standalone list.

        # Step 3: Reverse the second half of the list (head2)
        # Standard linked list reversal algorithm.
        prev_node = None
        current_node = head2
        while current_node:
            next_temp = current_node.next # Store the next node
            current_node.next = prev_node # Reverse current node's pointer
            prev_node = current_node      # Move prev_node one step forward
            current_node = next_temp      # Move current_node one step forward
        
        # 'prev_node' is now the new head of the reversed second half.
        head2_reversed = prev_node 

        # Step 4: Merge the two halves alternately
        # We interleave nodes from head1 (L0, L1, ...) and head2_reversed (Ln, Ln-1, ...).
        # The target result is: L0 -> Ln -> L1 -> Ln-1 -> L2 -> Ln-2 ...
        p1 = head1
        p2 = head2_reversed
        while p2: # Continue as long as there are nodes in the second (reversed) half
                  # (p1 might have more nodes in the middle for odd length lists, which is fine)
            
            # Store the next nodes of p1 and p2 before modifying current links
            next_p1 = p1.next 
            next_p2 = p2.next 

            # Reorder links:
            # 1. p1 (current node from first half) points to p2 (current node from reversed second half)
            # 2. p2 then points to next_p1 (the original next node of p1)
            p1.next = p2
            p2.next = next_p1
            
            # Move p1 and p2 to their respective next positions to continue merging
            p1 = next_p1
            p2 = next_p2
        
        # The function modifies the list in-place, so no explicit return value is needed.

# Helper functions for testing
def create_linked_list(arr):
    if not arr:
        return None
    head = ListNode(arr[0])
    current = head
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    return head

def linked_list_to_list(head):
    arr = []
    current = head
    while current:
        arr.append(current.val)
        current = current.next
    return arr

# Test Cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        ([], []),  # Empty list
        ([1], [1]), # Single node
        ([1, 2], [1, 2]), # Two nodes
        ([1, 2, 3, 4], [1, 4, 2, 3]), # Even number of nodes
        ([1, 2, 3, 4, 5], [1, 5, 2, 4, 3]), # Odd number of nodes
        ([1, 2, 3, 4, 5, 6], [1, 6, 2, 5, 3, 4]) # Another even number of nodes
    ]

    for input_list, expected_output in test_cases:
        head = create_linked_list(input_list)
        solution.reorderList(head)
        result = linked_list_to_list(head)
        print(f"Input: {input_list}, Reordered: {result}, Expected: {expected_output}")
        assert result == expected_output, f"Test failed for input {input_list}. Expected {expected_output}, Got {result}"
        print("Test passed!")

```