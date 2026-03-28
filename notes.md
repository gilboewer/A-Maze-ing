# Requirements (non-obvious):
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

# TODO:
- Look into mypy and typing module
- Make venv for dependency isolation during development
- Check if default needs to be selected when arg isnt valid file or do we just exit?

# Before submission:
- Check requirements then read through subject for missing stuff
- Finish and remove TOODs in code
