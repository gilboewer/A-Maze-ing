import subprocess
from src.mazegen import MazeGenerator
from src.loadconfig import load_config

# def test_output_file_integrity():
#     config = load_config()
#     MazeGenerator(config).generate(True)
#     result = subprocess.run(
#         ["python3", "output_validator.py"],
#         capture_output=True,
#         text=True
#     )
#     assert not result

def test_test():
    pass
