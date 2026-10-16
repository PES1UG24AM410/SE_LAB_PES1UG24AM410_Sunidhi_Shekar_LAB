# Reflection

## 1. Which issues were easiest and hardest to fix?

**Easiest:** style issues like unused imports, `== None` and the missing newline. The tool gives the exact line and the fix is simple.

**Hardest:** `eval`. Bandit suggests `ast.literal_eval`, but that cannot run `base_price * 0.90`.function was changed to take a discount percentage instead and updated the call in `main()`.

## 2. Did the tools give any false positives?

- Flake8 and Pylint said `base_price` was unused, but the `eval` string used it. The tools cannot see inside strings.
- Bandit rated MD5 as High, but hashing an item ID is not really a security use. I still switched to SHA-256 to be safe.

The tools also missed real problems: the secret key printed on screen, the wrong `total_sales` value, and `%d` cutting off decimals in prices. I found these by running the program and reading the code.

## 3. How would you use these tools in a real project?

I would run them in the editor, in a pre-commit check, and in CI on every pull request. The build should fail on Bandit findings or a low Pylint score. A real false positive can be ignored on one line with a comment explaining why.

## 4. What improved after the fixes?

- Pylint: 3.86 to 9.80. Bandit: 5 issues to 0. Flake8: 7 issues to 0.
- Security: no shell command, no `eval`, stronger hash and random, no secret key in the code.
- Readability: clear names and docstrings.
- Reliability: no shared default list, and the total is correct.

The program still gives the same results (price 22.5, 6 items).