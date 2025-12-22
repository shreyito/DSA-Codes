```python
import collections

class Solution:
    def findOrder(self, numCourses: int, prerequisites: list[list[int]]) -> list[int]:
        """
        Finds a valid order to take all courses given the total number of courses
        and a list of prerequisite pairs. If it's impossible to take all courses
        due to a cycle, an empty list is returned.

        This problem is a classic application of topological sorting. We use
        Kahn's algorithm (based on in-degrees) to solve it.

        Args:
            numCourses (int): The total number of courses, labeled from 0 to numCourses - 1.
            prerequisites (list[list[int]]): A list of prerequisite pairs, where
                                             prerequisites[i] = [ai, bi] means
                                             you must take course `bi` first if
                                             you want to take course `ai`.
                                             (i.e., `bi` -> `ai` in the graph).

        Returns:
            list[int]: An array of courses in a valid topological order.
                       If a cycle exists and no such order is possible, an empty list.
        """
        # 1. Build the graph (adjacency list) and calculate in-degrees for each course.
        # graph[course_A] will contain a list of courses that have course_A as a prerequisite.
        # e.g., if [1, 0] is a prerequisite, it means 0 -> 1.
        # So, graph[0] will include 1.
        adj_list = collections.defaultdict(list)
        in_degree = [0] * numCourses

        for course_b, course_a in prerequisites:
            # course_a is a prerequisite for course_b
            # Edge: course_a -> course_b
            adj_list[course_a].append(course_b)
            in_degree[course_b] += 1

        # 2. Initialize a queue with all courses that have an in-degree of 0.
        # These are the courses with no prerequisites, so they can be taken first.
        queue = collections.deque()
        for i in range(numCourses):
            if in_degree[i] == 0:
                queue.append(i)

        # 3. Process courses using Kahn's algorithm.
        course_order = []
        while queue:
            current_course = queue.popleft()
            course_order.append(current_course)

            # For each course that has `current_course` as a prerequisite:
            for neighbor_course in adj_list[current_course]:
                in_degree[neighbor_course] -= 1
                # If a neighbor course's in-degree becomes 0, it means all its
                # prerequisites have been met, so it can now be taken.
                if in_degree[neighbor_course] == 0:
                    queue.append(neighbor_course)

        # 4. Check for cycles.
        # If the length of the `course_order` list is less than `numCourses`,
        # it means there were courses left with non-zero in-degrees, implying
        # a cycle in the graph. In this case, it's impossible to take all courses.
        if len(course_order) == numCourses:
            return course_order
        else:
            return []

# Test Cases:
if __name__ == "__main__":
    solver = Solution()

    # Test Case 1: Basic case with a single prerequisite
    numCourses1 = 2
    prerequisites1 = [[1, 0]] # To take course 1, you must take course 0 first. (0 -> 1)
    # Expected: [0, 1]
    print(f"Test 1:")
    print(f"  numCourses: {numCourses1}, prerequisites: {prerequisites1}")
    print(f"  Order: {solver.findOrder(numCourses1, prerequisites1)}")
    print("-" * 30)

    # Test Case 2: More complex dependencies
    numCourses2 = 4
    prerequisites2 = [[1, 0], [2, 0], [3, 1], [3, 2]]
    # Graph: 0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3
    # Expected: [0, 1, 2, 3] or [0, 2, 1, 3] (any valid topological sort)
    print(f"Test 2:")
    print(f"  numCourses: {numCourses2}, prerequisites: {prerequisites2}")
    print(f"  Order: {solver.findOrder(numCourses2, prerequisites2)}")
    print("-" * 30)

    # Test Case 3: No prerequisites
    numCourses3 = 3
    prerequisites3 = []
    # Expected: [0, 1, 2] (or any permutation)
    print(f"Test 3:")
    print(f"  numCourses: {numCourses3}, prerequisites: {prerequisites3}")
    print(f"  Order: {solver.findOrder(numCourses3, prerequisites3)}")
    print("-" * 30)

    # Test Case 4: Cycle detected
    numCourses4 = 2
    prerequisites4 = [[1, 0], [0, 1]] # 0 -> 1, 1 -> 0 (cycle)
    # Expected: []
    print(f"Test 4 (Cycle):")
    print(f"  numCourses: {numCourses4}, prerequisites: {prerequisites4}")
    print(f"  Order: {solver.findOrder(numCourses4, prerequisites4)}")
    print("-" * 30)

    # Test Case 5: Another cycle
    numCourses5 = 3
    prerequisites5 = [[0, 1], [1, 2], [2, 0]] # 1 -> 0, 2 -> 1, 0 -> 2 (cycle)
    # Expected: []
    print(f"Test 5 (Cycle):")
    print(f"  numCourses: {numCourses5}, prerequisites: {prerequisites5}")
    print(f"  Order: {solver.findOrder(numCourses5, prerequisites5)}")
    print("-" * 30)

    # Test Case 6: Disjoint components
    numCourses6 = 4
    prerequisites6 = [[1, 0], [3, 2]] # 0 -> 1, 2 -> 3
    # Expected: [0, 2, 1, 3] or [2, 0, 3, 1] etc.
    print(f"Test 6 (Disjoint):")
    print(f"  numCourses: {numCourses6}, prerequisites: {prerequisites6}")
    print(f"  Order: {solver.findOrder(numCourses6, prerequisites6)}")
    print("-" * 30)

    # Test Case 7: Larger example
    numCourses7 = 5
    prerequisites7 = [[1,0],[2,0],[3,1],[4,2],[4,3]]
    # Graph: 0 -> 1, 0 -> 2, 1 -> 3, 2 -> 4, 3 -> 4
    # Expected: [0, 1, 2, 3, 4] or [0, 2, 1, 3, 4] (etc.)
    print(f"Test 7 (Larger):")
    print(f"  numCourses: {numCourses7}, prerequisites: {prerequisites7}")
    print(f"  Order: {solver.findOrder(numCourses7, prerequisites7)}")
    print("-" * 30)
```