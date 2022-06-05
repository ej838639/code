s_list = ['I', 'II', 'III', 'IV', 'V',
          'VI', 'VII', 'VIII', 'IX', 'X',
          'XI', 'XII', 'XIII', 'XIV', 'XV',
          'XVI', 'XVII', 'XVIII', 'XVIV', 'XX',
          'XXI', 'XXII', 'XXIII', 'XXIV', 'XXV',
          'XXVI', 'XXVII', 'XXVIII', 'XXVIV', 'XXX',
          'XXXI', 'XXXII', 'XXXIII', 'XXXIV', 'XXXV',
          'XXXVI', 'XXXVII', 'XXXVIII', 'XXXVIV', 'XL',
          'CM', 'XL', 'CMXL'
         ]


class Solution:
    def romanToInt(self, s: str) -> int:
        r2i_dict = {'I': 1, 'V': 5, 'X': 10,
                    'L': 50, 'C': 100, 'D': 500, 'M': 1000}

        solution = 0
        skip_flag = False

        if len(s) == 1:
            solution = r2i_dict[s[0]]

        else:
            for x in range(1, len(s)):
                # print('Start:', s, ':', x, ':', solution,
                # ':', skip_flag)
                if skip_flag == True:
                    skip_flag = False
                    continue

                if r2i_dict[s[x]] > r2i_dict[s[x - 1]]:
                    solution += r2i_dict[s[x]] - r2i_dict[s[x - 1]]
                    skip_flag = True
                    # print('Combo:', s, ':', x, ':', solution)

                else:
                    solution += r2i_dict[s[x - 1]]
                    skip_flag = False
                    # print('Single:', s, ':', x, ':', solution)

        if skip_flag == False and len(s) > 1:
            solution += r2i_dict[s[len(s) - 1]]

        return solution

solution = Solution()

for s in s_list:
    solution.romanToInt(s)
    print(s, solution.romanToInt(s))