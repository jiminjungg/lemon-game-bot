# 🍋 Lemon Game Bot

A Python script that automates playing [Lemon Game](https://wwme.kr/lemon/play?mode=normal), a Korean browser-based puzzle game.

It uses the [Playwright library](https://playwright.dev/python/docs/library) for browser interactions such as skipping ads and solving each board.

## Features

- Automates game startup, ad skipping, and gameplay
- Solves each board greedily, maximizing score and digit value
- Consistently ranks around 2,220th out of 14 million submissions

## Requirements

- [`uv`](https://docs.astral.sh/uv/)
- Google Chrome

## Installation

1. Clone this repository:

   ```sh
   git clone https://github.com/jiminjungg/lemon-game-bot.git
   cd lemon-game-bot
   ```

2. Install Chromium through Playwright if Google Chrome is not installed:

   ```sh
   uv run playwright install chromium
   ```

## Usage

Run the script:

```sh
uv run main.py
```

To play multiple games, use the `-n` or `--num_games` flag:

```sh
uv run main.py -n 3
```
