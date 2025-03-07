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
purpose. According to Balaji(2020), interior point method takes nearly twice
fast to run for a simpler problem than the simplex method and as the problem
gets larger it almost becomes ten times faster<a id="1">[1]</a>. Although the
algorithm is not as straight forward to understand than the simplex method, we
wanted to maximize the efficiency of our algorithm to account for potential
complications in problem building in a real life ride share problem.
Traditionally, interior point method was solved using direct linear solvers,
such as the LDL factorization for indefinite matrices or Cholesky factorization
for positive definite methods, but for sparse linear systems like ours,
iterative linear solvers are much more effective<a id="2">[2]</a>. Designing
interior point method with such considerations, we were able to find the optimum
solution for the assignment of rides and profit maximization in terms of
operational constraints such as total distance and number of trips.

## How It Works

![Interior Point Visualization](visualization.png)

Interior Point Methods work by initializing a feasible, and most likely
suboptimal, solution within the feasible region. They then iteratively move this
solution through the interior of the feasible region, gradually converging to
the optimal solution.

To prevent the solution from violating any constraints, a barrier function is
used to create a "force field" that keeps solutions away from constraint
boundaries and within the feasible region<a id="3">[3]</a>. The strength of this
barrier is controlled by a parameter $\mu$, which starts high and is
progressively reduced, allowing the solution to get closer to the boundaries as
it nears optimality.

But how does the algorithm know the direction in which to move the solution? To
find the optimal trajectory, the algorithm uses Newton's method to calculate a
search direction, iteratively improving the solution<a id="4">[4]</a>. However,
we can’t blindly move the solution in the direction of the optimal trajectory,
as this could lead to infeasibility (e.g., negative values for decision
variables). So, a step size is then determined to balance progress towards the
objective with maintaining feasibility.

This iterative process of minimizing the barrier function and optimizing the
objective creates what is referred to as a "central path" through the interior
of the feasible region, ultimately leading to the optimal solution.

## Solving a Problem

### Step 1: Problem Setup

The objective of this problem is to maximize profit from providing
transportation services, given constraints on distance and the total number of
trips. Three passenger types are available: long-distance passenger (50km, $40
profit), medium-distance passenger (30km, $20 profit), and short-distance
passenger (10km, $5 profit). The constraints are a maximum total distance of
1000 kilometers and a maximum of 20 total trips. The goal is to determine the
optimal number of each passenger type to maximize the total profit, subject to
these constraints and the non-negativity of the number of trips.

1. **Decision Variables**
   - $x_1$: Number of long-trip passengers
   - $x_2$: Number of medium-trip passengers
   - $x_3$: Number of short-trip passengers
2. **Objective Function**
   - Maximize profit: $z = 40x_1+20x_2+5x_3$
3. **Constraints**
   - Distance constraint: $50x_1+30x_2+10x_3 \le 1000$
   - Number of trips constraint: $x_1+x_2+x_3 \le 20$
   - Non-negativity: $x_1, x_2, x_3 \ge 0$

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

   $r_c = XS - \mu$

Here $X$ and $S$ are diagonal matrices with `x` and `s`along the diagonal. These
residuals form a system of equations that is solved at each iteration.

### Step 3: Solve the KKT System

The algorithm builds the Karush-Kuhn-Tucker (KKT), a block matrix that encodes
the relationships between primal variables, dual variables, and slack variables.
Solving this system simultaneously updates all variables, guiding the solution
toward optimality.

The KKT matrix is constructed to solve for search directions:

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

To update the variables, we solve the linear system, which finds a direction
that minimizes the residuals (i.e., the optimal trajectory).

### Step 4: Newton’s Method & Variable Updates

Blindly applying these variable updates can lead to infeasibility (e.g.,
negative values for decision variables). To prevent this, a step size is
determined by taking the largest possible fraction of the update that keeps all
variables positive.

$\alpha=0.99 \cdot \text{min}(1,\text{min}(-x/\Delta x))$\
$\beta=0.99 \cdot \text{min}(1,\text{min}(-s/\Delta s))$

This ensures that the algorithm does not step outside the feasible region. Then
we update the variables using our computed step sizes and search directions:

$x = x + \alpha \Delta x$\
$\lambda = \lambda + \beta \Delta \lambda$\
$s = s + \beta \Delta s$

To guide convergence, $\mu$ is gradually reduced by a factor of 0.1 in each
iteration. This allows the solution to approach the optimal point smoothly.

### Step 5: Convergence Check

The algorithm checks for convergence using three conditions:

- The primal residual is close to zero (constraints are satisfied).
- The dual residual is close to zero (optimality conditions are met).
- The $\mu$ parameter is close to zero.

If these conditions are met, the algorithm terminates, returning the optimal
solution. Otherwise, it iterates again.

### Design Decisions

- Using $r_c$ Instead of a Log Barrier Function: Traditional methods use a
  logarithmic barrier function to enforce positivity constraints, but this
  requires careful tuning of the barrier parameter. Instead, we use the residual
  $r_c$ directly, keeping the update process simpler.

- Reduction of $\mu$: Rather than adjusting $\mu$ based on problem progress, we
  reduce it by a fixed factor each iteration. This helps to avoid unnecessary
  parameter tuning and keeps behavior predictable.

- Simplified Line Search for Step Size: Instead of using complex backtracking
  line search methods to fine-tune step sizes, we take a heuristic approach that
  maintains feasibility with less computation. This results in slightly less
  precision, but makes up for it in code simplification.

### Other Applications
Interior point methods are useful for more than just ride share optimization problems. They are widely used to solve complex optimization problems in a number of different fields. They’re especially useful when dealing with large systems or problems that have lots of constraints. Some examples include:

- Finance: The goal is to pick a portfolio of assets that maximizes expected returns while keeping risk low, usually measured by the variance of portfolio returns. The constraints might include asset limits, regulations, and rules around diversification.

- Machine Learning: Typically used for large-scale regression problems like Lasso or Ridge regression. The goal is to find the optimal parameters of the model that minimize the loss function. The constraints in these cases typically involve limiting the complexity of the model, such as constraining the size of the coefficients through regularization terms.

- Robotics: Used for controlling robot movements and optimizing performance in real-time. The goal is to find the optimal control actions that minimize energy usage, maximize speed, or ensure precise movements. The constraints typically involve physical limitations (e.g., joint angles, speed limits), safety requirements (e.g., collision avoidance), and task-specific rules (e.g., maintaining balance or following a path).

In short, interior-point methods are incredibly versatile and can be applied to a wide range of optimization problems across different fields. Whether it's managing a portfolio, training machine learning models, or controlling robots, these methods help solve complex problems efficiently while handling a variety of constraints. Their ability to work with large systems and find optimal solutions in real-time makes them a powerful tool in many industries.

## Ethical Analysis

Interior point methods are powerful optimization tools, but they’re not free
from ethical concerns. Misuse can happen when these algorithms rely on already
biased data or constraints. For example, in resource allocation, if the input
data skews toward certain demographics, the algorithm can unintentionally
reinforce and even worsen those disparities. Most of the time, this bias isn’t
intentional; it comes from the data rather than the algorithm
itself<a id="5">[5]</a>. But in some cases, intentional misuse is possible, like
tweaking constraints or objective functions to favor certain groups.

A real-world example of this kind of issue is the COMPAS risk assessment tool
used to predict the potential for recidivism. While COMPAS doesn’t explicitly
use linear programming, it still suffers from a similar problem: biased data
leading to biased outcomes. Studies have shown that the algorithm
disproportionately categorizes Black defendants as high-risk for reoffending
<a id="6">[6]</a>. This happens because the historical data it was trained on
reflects systemic biases in the justice system, like conflating arrests with
convictions. The algorithm itself isn’t “racist,” but it learns patterns from
biased data, reinforcing the same disparities. To address these issues, it’s
crucial to audit data for biases, add fairness constraints to the optimization
process, and keep the algorithm’s decisions as transparent as possible.

## Resources

### Libraries

**required**

[NumPy](https://numpy.org/): `algorithms.py` and `applications.py`

**optional** - only used for verification of the algorithm.

[SciPy](https://scipy.org/): `verify_result.py`

### Research Links

<a id="1">[1]</a> Balaji, N. "Linear Programming Simplex and Interior Point
Methods – Indian Institute of Technology, Kanpur" Jun. 9, 2020. [Online].
Available: https://naveenbiitk.github.io/report/752.pdf

<a id="2">[2]</a> Saad, Y. "Iterative Methods for Sparse Linear Systems, Second
Edition" 2003 https://www-users.cse.umn.edu/~saad/IterMethBook_2ndEd.pdf

<a id="3">[3]</a> “Interior-point method for LP - Cornell University
Computational Optimization Open Textbook - Optimization Wiki.”
https://optimization.cbe.cornell.edu/index.php?title=Interior-point_method_for_LP

<a id="4">[4]</a> N. Jorge and S. J. Wright, Eds., “Chapter 14: Linear
Programming: Interior-Point Methods,” in Numerical Optimization, Springer New
York, NY. [Online]. Available:
https://pages.cs.wisc.edu/~swright/726/handouts/ip_h.pdf

<a id="5">[5]</a> S. Hajian, F. Bonchi, and C. Castillo, Algorithmic Bias: From
Discrimination Discovery to Fairness-aware Data Mining. Association for
Computing Machinery, 2016. doi: 10.1145/2939672.2945386.

<a id="6">[6]</a> J. L. A. Mattu Lauren Kirchner,Surya, “How we analyzed the
COMPAS Recidivism Algorithm,” ProPublica, Dec. 20, 2023. [Online]. Available:
https://www.propublica.org/article/how-we-analyzed-the-compas-recidivism-algorithm
