from sympy import symbols

# Define the numbers as symbols
x = symbols('x')

# Define the calculation
calculation = x * x

# Substitute x with 66666 and evaluate
result = calculation.subs(x, 66666)

# Print the result
print(result)
