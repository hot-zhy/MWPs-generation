import sympy as sp

# Safe environment setup
local_vars = {
    "sp": sp,
    "Eq": sp.Eq,
    "solve": sp.solve,
    "symbols": sp.symbols,
    # Provide a placeholder for the result to be stored
    "result": None
}

# SymPy code as a string, for example, received from an API response
# Removed the import statement and changed 'print' to an assignment to 'result'
sympy_code = """
# Define the number of students as a symbol
n = symbols('n')

# Original square (side^2) + surplus forms the initial number of students
original_square = Eq(n**2 + 5, n)

# A new larger square is (side + 1)^2, which requires 26 more students
larger_square = Eq((n + 1)**2, n + 26)

# Solve the system of equations
results = solve((original_square, larger_square), n)

# Filter the positive solution as the number of students has to be positive
result = [sol.evalf() for sol in results if sol.is_real and sol > 0][0]
"""


try:
    # Execute the sympy_code in a safe local environment
    exec(sympy_code, {"__builtins__": None}, local_vars)
except Exception as e:
    print(f"An error occurred: {e}")
else:
    # Retrieve the result after execution
    # Access the result directly since we know it's been defined
    result = local_vars['result']
    print(f"The result of the calculation is {result}")
