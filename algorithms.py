"""Interior point method algorithm implementation"""

import numpy as np

MUS = []
ITERATES = []


def interior_point(A, b, c, mu=1, tol=1e-6, max_iter=100):
    """
    An implementation of the interior point algorithm.
    Parameters:
        A: The matrix of constraint coefficients.
        b: The vector representing the constraint limits.
        c: The vector of objective function coefficients, representing the costs associated
            with each variable.
        mu: The barrier parameter (initial value).
        tol: Tolerance for convergence.
        max_iter: Maximum number of iterations.
    Returns:
        x: The solution vector, containing the decision variable values.
        x * c: The objective function value achieved with those decision variable values.
    """
    global MUS, ITERATES
    m, n = A.shape  # number of constraints, number of decision variables
    x = np.ones(n) * 0.5  # initial guess for the primal variables (decision variables)
    s = np.ones(n)  # initial guess for the slack variables
    lam = np.zeros(m)  # initial guess for the dual variables

    for k in range(max_iter):
        X = np.diag(x)  # diagonal matrix of primal variables
        S = np.diag(s)  # diagonal matrix of slack variables
        r_d = A.T @ lam + s - c  # dual residual
        r_p = A @ x - b  # primal residual
        r_c = X @ S @ np.ones(n) - mu * np.ones(n)  # complementarity residual

        # Check for convergence
        if np.linalg.norm(r_p) < tol and np.linalg.norm(r_d) < tol and mu < tol:
            ITERATES.append(x.copy())
            MUS.append(mu)
            print("Converged")
            return x, x * c  # optimal solution, profit

        # Build the KKT Matrix
        KKT = np.block(
            [
                [np.zeros((n, n)), A.T, np.eye(n)],
                [A, np.zeros((m, m)), np.zeros((m, n))],
                [S, np.zeros((n, m)), X],
            ]
        )

        # Build the right-hand side of the KKT system
        rhs = np.concatenate([-r_d, -r_p, -r_c])

        # Solve the KKT system for the search direction
        delta = np.linalg.solve(KKT, rhs)

        # Get the search directions for x, lambda, and s
        delta_x = delta[:n]
        delta_lam = delta[n : n + m]
        delta_s = delta[n + m :]

        # Line search to determine step size
        alpha = 0.99 * min(1, min(-x[delta_x < 0] / delta_x[delta_x < 0], default=1))
        beta = 0.99 * min(1, min(-s[delta_s < 0] / delta_s[delta_s < 0], default=1))

        # Update variables
        x += alpha * delta_x
        lam += beta * delta_lam
        s += beta * delta_s

        MUS.append(mu)

        # Reduce the barrier parameter
        mu *= 0.1

        ITERATES.append(x.copy())

        print(mu)

    print("Maximum iterations reached")
    return x, x * c
