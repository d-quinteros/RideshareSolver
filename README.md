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

## How It Works

Interior Point Methods work by initializing a feasible, and most likely suboptimal, solution within the feasible region. They then iteratively move this solution through the interior of the feasible region, gradually converging to the optimal solution.

To prevent the solution from violating any constraints, a barrier function is used to create a "force field" that keeps solutions away from constraint boundaries and within the feasible region. The strength of this barrier is controlled by a parameter $\mu$, which starts high and is progressively reduced, allowing the solution to get closer to the boundaries as it nears optimality.

But how does the algorithm know the direction in which to move the solution? To find the optimal trajectory, the algorithm uses Newton's method to calculate a search direction, iteratively improving the solution. However, we can’t blindly move the solution in the direction of the optimal trajectory, as this could lead to infeasibility (e.g., negative values for decision variables). So, a step size is then determined to balance progress towards the objective with maintaining feasibility.

This iterative process of minimizing the barrier function and optimizing the objective creates what is referred to as a "central path" through the interior of the feasible region, ultimately leading to the optimal solution.

## Solving a Problem
### Step 1: Problem Setup

The objective of this problem is to maximize profit from providing
transportation services, given constraints on distance and the total number of
trips. Three trip types are available: long-distance (50km, $40 profit),
medium-distance (30km, $20 profit), and short-distance (10km, $5 profit). The
constraints are a maximum total distance of 1000 kilometers and a maximum of 20
total trips. The goal is to determine the optimal number of each trip type to
maximize the total profit, subject to these constraints and the non-negativity
of the number of trips.

1. **Decision Variables**
   - $x_1$: Number of long-trip passengers
   - $x_2$: Number of medium-trip passengers
   - $x_3$: Number of short-trip passengers
2. **Objective Function**
   - Maximize profit:
     $z = 40x_1+20x_2+5x_3$
3. **Constraints**
   - Distance constraint:
     $50x_1+30x_2+10x_3 \le 1000$
   - Number of trips constraint:
     $x_1+x_2+x_3 \le 20$
   - Non-negativity:
     $x_1, x_2, x_3 \ge 0$

The cost vector `c` represents profit per passenger type, while `A` and `b`
define the constraint matrix and bounds. The algorithm initializes `x` (the
decision variables) to a small positive value to keep them strictly positive,
preventing division by zero later in the process. Slack variables `s` are
introduced to maintain feasibility, and the Lagrange multipliers `λ` (dual
variables) track constraint violations.

Slack variables play a crucial role in transforming inequality constraints into
equalities, making them easier to work with in a system of equations. So, an
inequality constraint such as:

$\text{distance constraint}: 50x_1+30x_2+10x_3 \le 1000$

would be rewritten using a slack variable `s_1` as:

$50x_1+30x_2+10x_3 +s_1 = 1000$

This helps to make sure that that the solution remains feasible while allowing
us to incorporate constraints directly into our iterative update process.

Lagrange multipliers help to measure how much the objective function would
improve if a constraint were slightly relaxed. Conceptually, they represent the
"pressure" that a constraint exerts on the solution

### Step 2: Iterative Optimization Process

At each iteration, the algorithm constructs three key residuals:

1. **Dual Residual (r_d)**: Measures the difference between the gradient of the
   Lagrangian and the actual cost vector. If this is nonzero, it means the
   current solution is not optimal.
   $r_d = A^T \lambda+s-c$
2. **Primal Residual (r_p)**: Represents how much the current solution violates
   the constraints. Ideally, this should be zero when the algorithm converges.
   $r_p = Ax -b$
3. **Complementary Slackness Residual (r_c)**: Ensures that slack variables `s`
   and decision variables `x` remain balanced.
   $r_c = XS - \mu$\
   Here $X$ and $S$ are diagonal matrices with `x` and `s`along the diagonal. These residuals form a system of equations that is solved at each iteration. 

### Step 3: Solve the KKT System
The algorithm builds the **KKT matrix**, a block matrix that encodes the relationships between primal variables, dual variables, and slack variables. Solving this system simultaneously updates all variables, guiding the solution toward optimality.

The Karush-Kuhn-Tucker (KKT) matrix is constructed to solve for search directions:

$$
\begin{bmatrix}
0 & A^T & I\\
A & 0 & 0\\
S & 0 & X
\end{bmatrix}
\begin{bmatrix}
\Delta x\\
\Delta \lambda\\
\Delta s
\end{bmatrix}=
\begin{bmatrix}
-r_d\\
-r_p\\
-r_c
\end{bmatrix}
$$

To update the variables, we solve the linear system, which finds a direction that minimizes the residuals (i.e., the optimal trajectory).

### Step 4: Newton’s Method & Variable Updates
Blindly applying these variable updates can lead to infeasibility (e.g., negative values for decision variables). To prevent this, a step size is determined by taking the largest possible fraction of the update that keeps all variables positive. 

$\alpha=0.99 \cdot \text{min}(1,\text{min}(-x/\Delta x))$
$\beta=0.99 \cdot \text{min}(1,\text{min}(-s/\Delta s))$

This ensures that the algorithm does not step outside the feasible region. Then we update the variables using our computed step sizes and search directions:

$x = x + \alpha \Delta x$
$\lambda = \lambda + \beta \Delta \lambda$
$s = s + \beta \Delta s$

To guide convergence, $\mu$ is gradually reduced by a factor of 0.1 in each iteration. This allows the solution to approach the optimal point smoothly.

### Step 5: Convergence Check
The algorithm checks for convergence using three conditions:
-   The primal residual is close to zero (constraints are satisfied).
-   The dual residual is close to zero (optimality conditions are met).
-   The complementarity condition is sufficiently small (primal and dual variables are properly balanced).

If these conditions are met, the algorithm terminates, returning the optimal solution. Otherwise, it iterates again.

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
