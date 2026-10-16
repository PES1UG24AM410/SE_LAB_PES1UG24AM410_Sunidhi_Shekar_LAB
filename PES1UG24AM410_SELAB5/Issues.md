# Issues Found in ecommerce_cart_system.py

Line numbers are from the original file.

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 3.86/10 | 9.80/10 |
| Bandit | 5 issues (2 High, 1 Medium, 2 Low) | 0 issues |
| Flake8 | 7 issues | 0 issues |

## Issue table

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| `os.system` with a string (B605) | Security, High | 60 | The filename goes into a shell command, so someone could inject extra commands. | Removed it and used `logging.info` to show the message. |
| MD5 hash (B324) | Security, High | 49 | MD5 is weak and not safe to use. | Switched to `hashlib.sha256`. |
| `eval()` (B307, W0123) | Security, Medium | 44 | `eval` runs any code it is given. | Replaced the expression with a number (`discount_percent`) and calculated the price directly. |
| Bare `except: pass` (B110, E722, W0702) | Bug, Low | 28 | Hides all errors silently. | Used `cart_items.pop(item_id, None)` instead of try/except. |
| `random` for PIN (B311) | Security, Low | 53 | `random` is predictable. | Used `secrets.randbelow`. |
| Hardcoded secret key | Security (no tool flagged it) | 72, 81 | The payment key is in the code and printed on screen. | Read it from an environment variable and stopped printing it. |
| Mutable default `audit_log=[]` (W0102) | Bug | 15 | The same list is shared between all calls. | Default is now `None`. |
| `total_sales` global (W0603) | Logic bug | 12, 16, 20 | Ignores starting items and removals, so it is wrong. | Removed it and added `get_cart_value()` to calculate the total. |
| `with` not used for file (R1732, W1514) | Quality | 57 | The file may stay open and no encoding is set. | Used `with open(..., encoding="utf-8")`. |
| `== None` (E711, C0121) | Style | 34 | Wrong way to check None. | Changed to `is None`. |
| Unused import and variables (F401, F841, W0611, W0612) | Style | 4, 33, 43, 65 | Code that is never used. | Removed them. |
| camelCase names (C0103) | Style | 15 to 63 | Python uses snake_case. | Renamed all functions. |
| Missing docstrings (C0114, C0116) | Style | many | No documentation. | Added docstrings. |
| Long line and no final newline (E501, W292) | Style | 76, 84 | Formatting problems. | Shortened the line and added a newline. |

## Fixes by commit

1. Bandit: `os.system`, MD5, `eval`, bare `except`, `random`, secret key.
2. Flake8: unused code, `== None`, long line, final newline.
3. Pylint: renames, docstrings, mutable default, `global`, `with open`.
