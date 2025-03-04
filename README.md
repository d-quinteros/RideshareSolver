# Ride Share Program Optimization

Sally Lee, DQ

## Background

Ride-sharing platforms such as Uber have the problem of optimally allocating
rides to achieve maximum profitability under the constraints of significant
operating limits such as distance, trips, and other resource limitations.
Optimization of such a variable is of great significance for maximizing the
overall system performance and customer satisfaction. As there has been a growth
in ride-sharing services, optimizing such problems becomes more complex with
multiple variables and constraints, thus higher-level algorithms need to be
applied for this.

In our project, we used the Interior Point Method (IPM) to optimize the
ride-sharing problem. It is a powerful algorithm for solving large-scale linear
and nonlinear convex optimization problems and therefore most apt for this
purpose. Utilizing IPM, we were able to find the optimum solution for the
assignment of rides and profit maximization in terms of operational constraints
such as total distance and number of trips.

## Walkthrough

## Solving a Problem

## Ethical Analysis

## Resources

### Libraries

**required**

[NumPy](https://numpy.org/): `algorithms.py` and `applications.py`

**optional** - only used for verification of the algorithm.

[SciPy](https://scipy.org/): `verify_result.py`

### Research links

[Cornell's interior point method for LP](https://optimization.cbe.cornell.edu/index.php?title=Interior-point_method_for_LP)
(Lauterio, Thakur, and Shenoy)
