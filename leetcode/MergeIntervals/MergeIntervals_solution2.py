from typing import List

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:

        intervals.sort(key=lambda x: x[0])

        merged = []
        for interval in intervals:
            # if the list of merged intervals is empty or if the current
            # interval does not overlap with the previous, simply append it.
            if not merged or merged[-1][1] < interval[0]:
                merged.append(interval)
            else:
            # otherwise, there is overlap, so we merge the current and previous
            # intervals.
                merged[-1][1] = max(merged[-1][1], interval[1])

        return merged

intervals_test = []
intervals_test.append([[1, 3], [2, 6], [8, 10], [15, 18]])
intervals_test.append([[1, 4], [2, 8], [8, 15], [15, 18]])
intervals_test.append([[1, 4], [4, 5]])
intervals_test.append([[1, 4], [0, 4]])
intervals_test.append([[1, 4], [2, 3]])
intervals_test.append([[2, 3], [4, 5], [6, 7], [8, 9], [1, 10]])

solution = Solution()
for i in range(len(intervals_test)):
    print('Test', i, 'Input: ', intervals_test[i])
    print('Test', i, 'Output:', solution.merge(intervals_test[i]), '\n')

print('Done')

