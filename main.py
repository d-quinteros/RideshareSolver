from applications import ride_share_problem
from algorithms import interior_point


def main():
    A, b, c = ride_share_problem()
    x_opt = interior_point(A, b, c)
    print("Optimal solution:", x_opt)


if __name__ == "__main__":
    main()
