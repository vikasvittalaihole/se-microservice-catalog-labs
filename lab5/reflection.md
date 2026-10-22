# Lab 5: Static Code Analysis - Reflection

## 1. What is static code analysis?

Static code analysis examines source code without executing it. It helps identify potential bugs, security vulnerabilities, maintainability problems, and style violations early in development.

## 2. What did the three tools help identify?

Pylint identified code-quality and maintainability issues. Bandit detected potentially insecure patterns, including unsafe expression evaluation, weak hashing, insecure random-number generation, shell execution, and a hardcoded token. Flake8 identified formatting violations, unused imports and variables, and exception-handling issues.

## 3. What improvements were made?

The code was updated to remove unsafe expression evaluation, use secure PIN generation, replace MD5 with SHA-256, remove shell execution, improve input validation, correct file handling, and follow Python naming and documentation conventions.

## 4. What did I learn from this lab?

I learned that code can run successfully while still containing security risks and maintainability problems. Using multiple static-analysis tools provides different perspectives on code quality. Rerunning the tools after making changes helps verify whether the reported issues have been addressed.

## Conclusion

The lab demonstrated how static-analysis tools can improve Python code quality, security, and maintainability before deployment.
