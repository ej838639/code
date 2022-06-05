from typing import List

class Solution:

    def merge(self, intervals: List[List[int]]) -> List[List[int]]:

        self.intervals = intervals
        self.intervals.sort(key=lambda x: x[0])
        self.intervals_len = len(intervals)
        self.intervals_combined = []
        self.count = 0

        while self.count < self.intervals_len:
            self.overlap_check()

        return self.intervals_combined

    def overlap_check(self):
        self.start = self.count

        if self.count > 0:
            intervals_combined_last = len(self.intervals_combined) - 1
            if self.intervals_combined[intervals_combined_last][1] >= self.intervals[self.count][0]:
                self.intervals_combined[intervals_combined_last][1] = self.intervals[self.count][1]
                self.count += 1
                return

        while self.count + 1 < self.intervals_len:
            if self.intervals[self.count][1] >= self.intervals[self.count + 1][0]:

                if self.intervals[self.count][1] >= self.intervals[self.count + 1][1]:
                    self.intervals_combined.append([self.intervals[self.start][0], self.intervals[self.count][1]])
                    self.count += 1
                else:
                    self.count += 1
                    self.intervals_combined.append([self.intervals[self.start][0], self.intervals[self.count][1]])

                self.count += 1
                return

            self.intervals_combined.append([self.intervals[self.count][0], self.intervals[self.count][1]])
            self.count += 1
            self.start += 1

        if self.count + 1 == self.intervals_len:
            self.intervals_combined.append([self.intervals[self.count][0], self.intervals[self.count][1]])
            self.count += 1

        return

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