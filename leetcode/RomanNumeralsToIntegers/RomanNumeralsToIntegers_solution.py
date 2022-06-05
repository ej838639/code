values = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}

class Solution:
    def romanToInt(self, s: str) -> int:
        total = 0
        i = 0
        while i < len(s):
            # If this is the subtractive case.
            if i + 1 < len(s) and values[s[i]] < values[s[i + 1]]:
                total += values[s[i + 1]] - values[s[i]]
                i += 2
            # Else this is NOT the subtractive case.
            else:
                total += values[s[i]]
                i += 1
        return total

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

solution = Solution()

for s in s_list:
    solution.romanToInt(s)
    print(s, solution.romanToInt(s))

print('Done')