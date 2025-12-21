```python
import heapq

class Solution:
    def scheduleCourse(self, courses: list[list[int]]) -> int:
        """
        Problem: Course Schedule III

        There are n courses labeled from 1 to n. You are given an array courses where
        courses[i] = [duration_i, lastDay_i] indicates that the ith course should be
        taken for duration_i days and must be finished before or on lastDay_i.

        You and I can only take one course at a time.

        Return the maximum number of courses that can be taken.

        Example 1:
        Input: courses = [[100,200],[200,1300],[1000,1250],[2000,3200]]
        Output: 3
        Explanation:
        Let's trace the solution with this example:
        Courses: [[100,200], [200,1300], [1000,1250], [2000,3200]]

        1. Sort courses by their lastDay (deadline) in ascending order:
           Sorted courses: [[100,200], [1000,1250], [200,1300], [2000,3200]]

        2. Initialize `current_time = 0` (total duration of courses taken) and
           `taken_durations = []` (a min-heap to store negative durations of courses taken).

        3. Process sorted courses one by one:

           - Course [100,200]:
             `current_time` (0) + `duration` (100) = 100.
             Is 100 <= `lastDay` (200)? Yes.
             Take this course:
               `current_time = 100`.
               `heapq.heappush(taken_durations, -100)`. `taken_durations` is now `[-100]`.

           - Course [1000,1250]:
             `current_time` (100) + `duration` (1000) = 1100.
             Is 1100 <= `lastDay` (1250)? Yes.
             Take this course:
               `current_time = 1100`.
               `heapq.heappush(taken_durations, -1000)`. `taken_durations` is now `[-1000, -100]` (heap property may reorder, but -1000 is min).

           - Course [200,1300]:
             `current_time` (1100) + `duration` (200) = 1300.
             Is 1300 <= `lastDay` (1300)? Yes.
             Take this course:
               `current_time = 1300`.
               `heapq.heappush(taken_durations, -200)`. `taken_durations` is now `[-1000, -100, -200]` (min element is -1000).

           - Course [2000,3200]:
             `current_time` (1300) + `duration` (2000) = 3300.
             Is 3300 <= `lastDay` (3200)? No. Cannot take directly.
             Check for replacement:
               Is `taken_durations` not empty? Yes (`[-1000, -100, -200]`).
               Is `duration` (2000) < `-taken_durations[0]` (which is `-(-1000) = 1000`)? No, 2000 is not < 1000.
               So, no replacement is made. This course is skipped.

        4. Final result: The number of courses taken is `len(taken_durations)`, which is 3.

        Explanation for the greedy strategy:
        1.  **Sort by `lastDay`**: Sorting courses by their deadlines ensures that we prioritize courses that have less flexibility. By considering courses with earlier deadlines first, we make sure to fit them if possible. If a course with an early deadline cannot be fit, it's a strong indication that our current schedule might need adjustment.

        2.  **Maintain `current_time` and a Max-Heap of Durations**:
            - `current_time` tracks the total accumulated duration of all courses currently in our schedule.
            - `taken_durations` is a min-heap where we store the *negative* durations of courses we have taken. Storing negative durations effectively turns a min-heap into a max-heap for the absolute values (durations). This allows us to efficiently retrieve and remove the course with the longest duration (`-heapq.heappop(taken_durations)`).

        3.  **Iterate and Decide**: For each course `[duration, lastDay]` in the sorted list:
            a.  **Can we take it directly?** If `current_time + duration <= lastDay`, we can simply add this course. We update `current_time` and add its negative duration to `taken_durations`. This increases the count of courses taken.
            b.  **Cannot take directly; consider replacement**: If `current_time + duration > lastDay`, the current course doesn't fit with our existing schedule. However, we might be able to swap it with one of the courses we've already taken. To maximize our chances of fitting the current course (and future courses), we want to free up as much time as possible. This means we should replace an existing course with the *longest duration* (`d_old`) with the current course (`d_new`), *but only if the current course is shorter* (`d_new < d_old`).
                -   If `taken_durations` is not empty AND `duration < -taken_durations[0]` (meaning `d_new < d_old_max`), then:
                    -   Remove the longest duration course (`d_old_max`) from `taken_durations` and subtract its duration from `current_time`.
                    -   Add the current course (`d_new`) to `taken_durations` (as `-d_new`) and add its duration to `current_time`.
                This operation keeps the number of courses taken the same but reduces `current_time`, making it easier for subsequent courses to fit. If `d_new >= d_old_max`, replacing would not help or would make it worse, so we simply skip the current course.

        4.  **Final Count**: The total number of courses we've managed to fit into the schedule is simply the number of elements in `taken_durations`.

        Time Complexity:
        O(N log N)
        -   Sorting the `courses` list takes O(N log N) time, where N is the number of courses.
        -   Iterating through N courses, each `heapq.heappush` or `heapq.heappop` operation on the `taken_durations` heap takes O(log K) time, where K is the current number of courses in the heap (at most N).
        -   Thus, the loop part takes N * O(log N) time.
        -   The dominant factor is O(N log N).

        Space Complexity:
        O(N)
        -   The `taken_durations` heap can store up to N course durations in the worst case.
        -   Python's `list.sort()` (Timsort) uses O(N) auxiliary space in the worst case.
        -   Therefore, the total space complexity is O(N).
        """
        # 1. Sort courses by their lastDay (deadline) in ascending order.
        # This ensures we prioritize courses that have less flexibility.
        courses.sort(key=lambda x: x[1])

        # `current_time` tracks the total duration of courses taken so far.
        current_time = 0
        # `taken_durations` is a min-heap to store the durations of courses we've committed to.
        # We store negative durations to effectively make it a max-heap for durations.
        # This way, `heapq.heappop(taken_durations)` will always give us the largest duration
        # among the taken courses (as it pops the smallest negative number, which corresponds
        # to the largest positive duration).
        taken_durations = []

        # 2. Iterate through the sorted courses
        for duration, lastDay in courses:
            # 3a. Try to take the current course directly
            if current_time + duration <= lastDay:
                current_time += duration
                heapq.heappush(taken_durations, -duration)
            # 3b. If the current course cannot be taken directly,
            # check if we can replace an already taken course with the current one.
            # We want to replace the longest duration course currently taken,
            # but only if the current course is shorter (to free up time).
            elif taken_durations and duration < -taken_durations[0]:
                # Remove the longest duration course from our schedule (from the heap).
                # `taken_durations[0]` is the smallest negative value, so `-taken_durations[0]`
                # is the largest positive duration.
                longest_taken_duration = -heapq.heappop(taken_durations)
                
                # Update current_time by first removing the old course's duration
                current_time -= longest_taken_duration
                
                # Then add the new course's duration
                current_time += duration
                
                # Add the new course's (negative) duration to the heap.
                heapq.heappush(taken_durations, -duration)
        
        # 4. The number of courses taken is the size of the heap.
        return len(taken_durations)


if __name__ == '__main__':
    solver = Solution()

    # Test Case 1: Example from problem description
    courses1 = [[100, 200], [200, 1300], [1000, 1250], [2000, 3200]]
    expected1 = 3
    result1 = solver.scheduleCourse(courses1)
    print(f"Test Case 1: {courses1}")
    print(f"Expected: {expected1}, Got: {result1}")
    assert result1 == expected1, f"Test Case 1 Failed: Expected {expected1}, Got {result1}"

    # Test Case 2: No courses
    courses2 = []
    expected2 = 0
    result2 = solver.scheduleCourse(courses2)
    print(f"Test Case 2: {courses2}")
    print(f"Expected: {expected2}, Got: {result2}")
    assert result2 == expected2, f"Test Case 2 Failed: Expected {expected2}, Got {result2}"

    # Test Case 3: Only one course, fits
    courses3 = [[10, 20]]
    expected3 = 1
    result3 = solver.scheduleCourse(courses3)
    print(f"Test Case 3: {courses3}")
    print(f"Expected: {expected3}, Got: {result3}")
    assert result3 == expected3, f"Test Case 3 Failed: Expected {expected3}, Got {result3}"

    # Test Case 4: Only one course, doesn't fit (duration > lastDay, but problem guarantees duration <= lastDay)
    # This scenario is invalid by problem constraints: `duration_i <= lastDay_i`
    # Let's use a scenario where it can't be taken due to 'current_time' even if duration <= lastDay (e.g. current_time starts > 0)
    # But current_time starts at 0, so any single course with duration <= lastDay will always fit.
    # So this test case is replaced with a more complex one below.

    # Test Case 5: Multiple courses, none fit due to conflicting deadlines/durations
    courses5 = [[1, 1], [1, 1], [1, 1]]
    expected5 = 1 # Can only take one course [1,1]
    result5 = solver.scheduleCourse(courses5)
    print(f"Test Case 5: {courses5}")
    print(f"Expected: {expected5}, Got: {result5}")
    assert result5 == expected5, f"Test Case 5 Failed: Expected {expected5}, Got {result5}"

    # Test Case 6: Courses where replacement is beneficial
    courses6 = [[5, 5], [6, 6], [4, 7]] # Sorted: [[5,5], [6,6], [4,7]]
    # 1. Take [5,5]. current_time=5. heap=[-5]
    # 2. Try [6,6]. 5+6=11 > 6. Cannot take. Heap: [-5]. current_time=5.
    # 3. Try [4,7]. 5+4=9 > 7. Cannot take directly.
    #    Check replace: duration 4 < -heap[0] (which is 5). Yes.
    #    Pop -5. current_time = 5 - 5 = 0.
    #    Add 4. current_time = 0 + 4 = 4. Push -4. Heap: [-4].
    expected6 = 1 # The course [4,7] is taken
    result6 = solver.scheduleCourse(courses6)
    print(f"Test Case 6: {courses6}")
    print(f"Expected: {expected6}, Got: {result6}")
    assert result6 == expected6, f"Test Case 6 Failed: Expected {expected6}, Got {result6}"

    # Test Case 7: All courses can be taken
    courses7 = [[1, 2], [2, 4], [3, 6]]
    # Sorted: [[1,2], [2,4], [3,6]]
    # 1. Take [1,2]. time=1. heap=[-1]
    # 2. Take [2,4]. time=1+2=3. heap=[-1,-2]
    # 3. Take [3,6]. time=3+3=6. heap=[-1,-2,-3]
    expected7 = 3
    result7 = solver.scheduleCourse(courses7)
    print(f"Test Case 7: {courses7}")
    print(f"Expected: {expected7}, Got: {result7}")
    assert result7 == expected7, f"Test Case 7 Failed: Expected {expected7}, Got {result7}"

    # Test Case 8: Many courses, complex replacements
    courses8 = [[7,17],[3,12],[10,20],[9,10],[5,20],[10,19],[4,18]]
    # Sorted by deadline:
    # [[9,10], [3,12], [7,17], [4,18], [10,19], [10,20], [5,20]]
    # 1. [9,10]: time=9, heap=[-9]
    # 2. [3,12]: time=9+3=12 <= 12. time=12, heap=[-9,-3]
    # 3. [7,17]: time=12+7=19 > 17. Replace? 7 < -heap[0](9). Yes.
    #    Pop -9. time=12-9=3. Add 7. time=3+7=10. Push -7. heap=[-7,-3]
    # 4. [4,18]: time=10+4=14 <= 18. time=14, heap=[-7,-4,-3]
    # 5. [10,19]: time=14+10=24 > 19. Replace? 10 < -heap[0](7). No. Skip.
    # 6. [10,20]: time=14+10=24 > 20. Replace? 10 < -heap[0](7). No. Skip.
    # 7. [5,20]: time=14+5=19 <= 20. time=19, heap=[-7,-5,-4,-3]
    expected8 = 4
    result8 = solver.scheduleCourse(courses8)
    print(f"Test Case 8: {courses8}")
    print(f"Expected: {expected8}, Got: {result8}")
    assert result8 == expected8, f"Test Case 8 Failed: Expected {expected8}, Got {result8}"

    print("\nAll test cases passed!")

```