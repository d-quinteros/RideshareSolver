"""Ride share problem application"""

import numpy as np


def ride_share_problem():
    """
    Defining the ride share problem variables.
    Parameters:
        A: The matrix of constraint coefficients.
        b: The vector representing the constraint limits.
        c: The vector of objective function coefficients, representing the costs associated
            with each variable.
    """
    A = np.array([[50, 30, 10], [1, 1, 1]])
    b = np.array([1000, 20])
    c = np.array([40, 20, 5])
    return A, b, c
