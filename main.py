# main.py - the entry point; it USES the calculator module
# "from <module> import <names>": module = file name WITHOUT .py (calculator.py would fail)
# both files must sit in the same folder so Python can find calculator
from calculator import addition, calcBmi


x = addition(23,34)   # call the imported function; 23 + 34 = 57
print(x)



res = calcBmi(100 , 1.80)   # 100 kg, 1.80 m -> 100 / 3.24 = ~30.86
print(res)
