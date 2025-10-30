# Auto Nonogram Solver

This repository contains an automatic script for solving nonograms on [puzzle-nonograms.com](https://puzzle-nonograms.com). The script is implemented in `auto_nonogram.py`.

## How to Use

1. **Run the Script**  
    Simply execute the script by running the following command in your terminal:  
    ```bash
    python auto_nonogram.py
    ```

2. **Login with Your Account**  
    To use your own account, fill in your cookies in the `cookie_template.json` file. After that, rename the file to `cookie.json`. This will allow the script to log in to your account.

## Hyperparameters

The script includes several hyperparameters that you can adjust to customize its behavior:

- **`SIZE`**: The size of the puzzle grid to solve. Supported values are `5`, `10`, `15`, `20`, and `25`.
- **`RANDOM_WAIT`**: If set to `True`, introduces random delays between actions to mimic human behavior.
- **`LOGIN`**: If set to `True`, the script will use the cookies in `cookie.json` to log in to your account.
- **`SLEEP_MIN`** and **`SLEEP_MAX`**: The minimum and maximum random wait times (in seconds) between actions when `RANDOM_WAIT` is enabled.
- **`ITERATE`**: The number of puzzles the script will attempt to solve in one session.

Feel free to tweak these parameters in the script to suit your preferences.

## Disclaimer

This script is for educational purposes only. Use it responsibly and ensure compliance with the terms of service of [www.puzzle-nonograms.com](https://www.puzzle-nonograms.com).  
