import argparse


def main() -> None:
    parser = argparse.ArgumentParser(
        description="A script that plays Lemon Game through browser automation"
    )
    parser.add_argument(
        "-n",
        "--num_games",
        default=1,
        type=int,
        help="number of times to play Lemon Game (default: %(default)s)",
    )

    args = parser.parse_args()


if __name__ == "__main__":
    main()
