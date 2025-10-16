import argparse
import re

from playwright.sync_api import Page, sync_playwright

AD_LOAD_TIMEOUT = 5000
AD_SKIP_TIMEOUT = 32000
GAME_LOAD_TIMEOUT = 3000
LEMON_GAME_URL = "https://wwme.kr/lemon/play?mode=normal#goog_rewarded"


def skip_ad(page: Page, is_first_skip: bool) -> None:
    page.wait_for_timeout(AD_LOAD_TIMEOUT)
    if is_first_skip:
        ad_dialogue_child = page.get_by_text("광고 시청하기")
        page.get_by_role("button").filter(has=ad_dialogue_child).click()
    ad_view_child = page.get_by_text("광고 보기")
    page.get_by_role("button").filter(has=ad_view_child).last.click()
    page.wait_for_timeout(AD_SKIP_TIMEOUT)
    ad_frame = page.get_by_title("3rd party ad content").last.content_frame
    ad_frame.get_by_role("button", name="동영상 닫기").click()
    page.get_by_text("확인").click()


def play_lemon_game(page: Page) -> None:
    game_start_child = page.get_by_text(re.compile(r"게임 시작|다시하기"))
    page.get_by_role("button").filter(has=game_start_child).click()
    page.wait_for_timeout(GAME_LOAD_TIMEOUT)


def run_lemon_game_bot(num_games: int) -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome", args=["--start-maximized"], headless=False
        )
        page = browser.new_page(no_viewport=True)
        page.goto(LEMON_GAME_URL)
        for i in range(num_games):
            if i % 10 == 0:
                skip_ad(page, i == 0)
            play_lemon_game(page)
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
