import numpy as np


def interior_point(A, b, c, mu=1, tol=1e-6, max_iter=100):
    """
    Interior point algorithm
    Params:
        A: Constraint matrix
        b: Constraint bounds
        c: cost vector
    Returns:
        x: the solution
    """
    m, n = A.shape  # number of constraints, number of decision variables
    x = np.ones(n) * 0.5  # initial guess
    s = np.ones(n)  # slack variables
    lam = np.zeros(m)

    for k in range(max_iter):
        X = np.diag(x)
        S = np.diag(s)
        r_d = A.T @ lam + s - c
        r_p = A @ x - b
        r_c = X @ S @ np.ones(n) - mu * np.ones(n)

        if np.linalg.norm(r_p) < tol and np.linalg.norm(r_d) < tol and mu < tol:
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

        rhs = np.concatenate([-r_d, -r_p, -r_c])
        delta = np.linalg.solve(KKT, rhs)

        delta_x = delta[:n]
        delta_lam = delta[n : n + m]
        delta_s = delta[n + m :]

        # Line search
        alpha = 0.99 * min(1, min(-x[delta_x < 0] / delta_x[delta_x < 0], default=1))
        beta = 0.99 * min(1, min(-s[delta_s < 0] / delta_s[delta_s < 0], default=1))

        # Update variables
        x += alpha * delta_x
        lam += beta * delta_lam
        s += beta * delta_s
        mu *= 0.1

    print("Maximum iterations reached")
    return x, x * c
