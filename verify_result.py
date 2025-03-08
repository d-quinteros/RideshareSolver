"""Verification of the interior point method algorithm using scipy"""

from scipy.optimize import linprog

# Coefficients of the objective function (maximize profit)
c = [-40, -20, -5]  # Use negative for maximization in scipy

# Coefficients of the constraints
A = [[50, 30, 10], [1, 1, 1]]
b = [1000, 20]

# Bounds for x1, x2, x3 (Non-negativity constraint)
x_bounds = (0, None)

# Solving
result = linprog(
    c, A_ub=A, b_ub=b, bounds=[x_bounds, x_bounds, x_bounds], method="simplex"
)

if result.success:
    print("Optimal Solution Found:")
    print("x1:", result.x[0])
    print("x2:", result.x[1])
    print("x3:", result.x[2])
    print("Max Profit:", -result.fun)
else:
    print("No Solution Found")
