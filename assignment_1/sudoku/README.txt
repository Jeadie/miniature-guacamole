# Sudoku CSP

There are three python files used to implement CSP for Sudokus:
* data_loader.py:
* backtracking_template.py:
* testing.py:


## Example usage (CLI):
There are four ways to run TSPs:

    1. Run a single Sudoku file. `python testing.py run <FILENAME>`
      Optional flags:
      * `--forward`: Uses forward checking
      * `--heuristics`: Uses further heuristics

    2. Run all Sudoku files from 1->n. `python testing.py all n`
      Optional flags:
      * `--forward`: Uses forward checking
      * `--heuristics`: Uses further heuristics

    3. Runs all Sudoku files from 1->n for all three models: `python testing.py compare n`

    4. Run a single Sudoku file against all three models. `python testing.py compare_file <FILENAME>`
