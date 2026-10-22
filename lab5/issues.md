## 3. Issues Identified and Fixes Applied

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Weak MD5 hashing | Security - High | 49 | MD5 is considered weak for security-sensitive hashing. | Replaced MD5 with SHA-256. |
| Shell command execution | Security - High | 60 | `os.system()` executes a shell command and can introduce command-injection risks. | Removed shell execution and reported export completion directly. |
| Unsafe `eval()` | Security - Medium | 44 | `eval()` executes a supplied expression and can execute unintended code. | Replaced dynamic evaluation with direct GPA calculation. |
| Hardcoded portal token | Security - Low | 64 | A token-like value was embedded directly in the source code. | Read the token from an environment variable and stopped printing its value. |
| Insecure random PIN generation | Security - Low | 53 | `random.randint()` is not intended for security-sensitive random values. | Replaced it with `secrets.randbelow()`. |
| Bare exception handling | Code quality / Security | 26 | A bare `except` catches errors too broadly and silently ignores them. | Replaced exception-based handling with input validation. |
| Mutable default argument | Code quality | 15 | The default list can be shared between function calls. | Changed the default to `None` and initialized a new list when needed. |
| Comparison with `None` | Code quality | 32 | Comparing a value to `None` using `==` is discouraged. | Used an `is None` check. |
| Unused variables | Code quality | 31, 43 | Variables were assigned but not used. | Removed the unused variables. |
| File handling without encoding or context manager | Code quality | 57 | The file was opened without an explicit encoding and closed manually. | Used `with open()` and UTF-8 encoding. |
| Unused import | Code quality | 6 | The `json` module was imported but never used. | Removed the unused import. |
| Naming, documentation, and formatting problems | Maintainability / Style | 15, 19, 23, 30, 35, 41, 48, 52, 56, 63, 75 | The original code had a nonstandard function name, missing docstrings, unnecessary conditional logic, long lines, and no final newline. | Renamed the function to `add_grade`, added docstrings, simplified returns, and corrected formatting. |
