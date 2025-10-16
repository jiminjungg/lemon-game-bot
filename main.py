import argparse

from playwright.sync_api import sync_playwright

LEMON_GAME_URL = "https://wwme.kr/lemon/play?mode=normal#goog_rewarded"


def run_lemon_game_bot(num_games: int) -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome", args=["--start-maximized"], headless=False
        )
        page = browser.new_page(no_viewport=True)
        page.goto(LEMON_GAME_URL)
        browser.close()


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
    run_lemon_game_bot(args.num_games)


if __name__ == "__main__":
    main()
