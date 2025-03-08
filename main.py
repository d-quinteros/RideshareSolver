"""Main file to run interior point method to the ride share problem"""

import numpy as np
import matplotlib.pyplot as plt
from applications import ride_share_problem
from algorithms import MUS, ITERATES, interior_point


def main():
    """
    main function to run the interior point method to the ride share problem and visualize.
    """
    A, b, c = ride_share_problem()
    x_opt, profits = interior_point(A, b, c)
    print("Optimal solution:", x_opt)
    print("Max Profit:", sum(profits))

    visualize(MUS, ITERATES)


def visualize(mus, iterates):
    """
    visualize how algorithms works for the ride share problem.
    Parameters:
        mus: list of mus at each iteration
        iterates: list of iterates showing the 3D coordinates.
    """

    iterates = np.array(iterates)
    mus = np.array(mus)
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(projection="3d")
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.set_zlabel("x3")
    ax.set_title("Interior Point Method Visualization")

    # Plot constraints
    x1 = np.linspace(0, 20, 100)
    x2 = np.linspace(0, 20, 100)
    X1, X2 = np.meshgrid(x1, x2)
    X3_dist = (1000 - 50 * X1 - 30 * X2) / 10
    X3_trips = 20 - X1 - X2

    ax.plot_surface(
        X1, X2, X3_dist, color="blue", alpha=0.3, label="50x1 + 30x2 + 10x3 <= 1000"
    )
    ax.plot_surface(
        X1, X2, X3_trips, color="green", alpha=0.3, label="x1 + x2 + x3 <= 20"
    )

    # Plot iterates
    ax.plot(
        iterates[:, 0],
        iterates[:, 1],
        iterates[:, 2],
        "ro-",
        label="Interior Point Iterates",
    )

    # Show mu values at each step
    for i, _ in enumerate(mus):
        ax.text(
            iterates[i, 0],
            iterates[i, 1],
            iterates[i, 2],
            f"μ={mus[i]:.1e}",
            fontsize=8,
        )

    ax.legend()
    plt.show()


if __name__ == "__main__":
    main()
