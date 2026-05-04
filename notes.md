# Requirements (non-obvious)
## General
- Include docstrings in functions and classes following PEP 257 (e.g., Google or NumPy style) to document purpose, parameters, and returns.
- Your code must include type hints for function parameters, return types, and variables where applicable (using the typing module). Use mypy for static type check- ing. All functions must pass mypy without errors.
- Makefile - See subject
- Create test programs to verify project functionality (not submitted or graded). Use frameworks like pytest or unittest for unit tests, covering edge cases.
- Include a .gitignore file to exclude Python artifacts.

## Project
- A default configuration file must be available in your Git repository
- Lines starting with # in the config file are comments and must be ignored
- Must use default config if none is specified

# TODO
- Makefile
  - pip install
- Testing framework
- Make venv for dependency isolation during development
- docstrings for everything, according to some guidelines (check also Kevins)
    - "Include docstrings in functions and classes following PEP 257 (e.g., Google or
        NumPy style) to document purpose, parameters, and returns."

# Before submission
- Finish and remove TOODs in code
- Check if everything works on pc in 42, including Makefile

# Note:
- If adding new config settings, make sure to validate them
