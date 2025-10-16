import argparse
import re

from playwright.sync_api import Locator, Page, sync_playwright

AD_LOAD_TIMEOUT = 5000
AD_SKIP_TIMEOUT = 32000
GAME_LOAD_TIMEOUT = 3000
LEMON_GAME_URL = "https://wwme.kr/lemon/play?mode=normal#goog_rewarded"
NUM_COLS = 17
NUM_ROWS = 10


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


def crawl_board(page: Page) -> list[list[list[int, bool, Locator]]]:
    cell_locators = page.locator(".cell").all()
    return [
        [
            [int(c.text_content()), c.get_attribute("data-lemon") == "true", c]
            for c in cell_locators[i : i + NUM_COLS]
        ]
        for i in range(0, len(cell_locators), NUM_COLS)
    ]


def get_valid_moves(
    board: list[list[list[int, bool, Locator]]],
) -> list[tuple[int, int, int, int]]:
    valid_moves = []
    for r1 in range(NUM_ROWS):
        prefix = [0] * NUM_COLS
        for r2 in range(r1, NUM_ROWS):
            for c in range(NUM_COLS):
                prefix[c] += board[r2][c][0]
            c1 = curr = 0
            for c2 in range(NUM_COLS):
                curr += prefix[c2]
                while curr >= 10:
                    while curr == 10 and prefix[c1] == 0:
                        c1 += 1
                    if curr == 10:
                        valid_moves.append((r1, c1, r2, c2))
                    curr -= prefix[c1]
                    c1 += 1
    return valid_moves


def evaluate_move(
    board: list[list[list[int, bool, Locator]]], move: tuple[int, int, int, int]
) -> tuple[int, int]:
    r1, c1, r2, c2 = move
    move_digit = move_score = 0
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            digit, lemon = board[r][c][0], board[r][c][1]
            if digit != 0:
                move_digit = max(move_digit, digit)
                move_score += 5 if lemon else 1
    return move_digit, move_score


def apply_move(
    board: list[list[list[int, bool, Locator]]], move: tuple[int, int, int, int]
) -> None:
    r1, c1, r2, c2 = move
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            board[r][c][0] = 0


def solve_board(
    board: list[list[list[int, bool, Locator]]],
) -> list[tuple[int, int, int, int]]:
    solution = []
    while True:
        valid_moves = get_valid_moves(board)
        if not valid_moves:
            return solution
        best_move, best_score, max_digit = (), 0, 0
        for move in valid_moves:
            move_digit, move_score = evaluate_move(board, move)
            if move_score > best_score:
                best_move = move
                best_score = move_score
                max_digit = move_digit
            elif move_score == best_score and move_digit > max_digit:
                best_move = move
                max_digit = move_digit
        solution.append(best_move)
        apply_move(board, best_move)


def apply_solution(
    board: list[list[list[int, bool, Locator]]],
    solution: list[tuple[int, int, int, int]],
) -> None:
    for r1, c1, r2, c2 in solution:
        top_left_cell, bottom_right_cell = board[r1][c1][2], board[r2][c2][2]
        top_left_cell.drag_to(bottom_right_cell)


def play_lemon_game(page: Page) -> None:
    game_start_child = page.get_by_text(re.compile(r"게임 시작|다시하기"))
    page.get_by_role("button").filter(has=game_start_child).click()
    page.wait_for_timeout(GAME_LOAD_TIMEOUT)
    board = crawl_board(page)
    apply_solution(board, solve_board(board))
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
