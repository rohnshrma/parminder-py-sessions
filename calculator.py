# calculator.py - a MODULE: any .py file whose functions other files can import

def addition(a,b):
    # return sends the result back to whoever called the function
    return a + b


def calcBmi(weight , height):
    # BMI = weight (kg) / height (m) squared; ** is the power operator
    return weight / height ** 2
