from typing import List

class Solution:
    def fizzBuzz(self, n: int) -> List[str]:
        answer = [*range(1, n + 1)]
        i_list = [*range(n)]
        for i in i_list:
            if answer[i] % 3 == 0 and answer[i] % 5 == 0:
                answer[i] = 'FizzBuzz'
            elif answer[i] % 3 == 0:
                answer[i] = 'Fizz'
            elif answer[i] % 5 == 0:
                answer[i] = 'Buzz'
            else:
                answer[i] = str(i+1)
        return answer

n = 15
solution = Solution()
print(n, '->', solution.fizzBuzz(n))

print('Done')
