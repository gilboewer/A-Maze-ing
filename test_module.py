from mazegen import MazeGenerator
from errors import ConfigValueError
import pytest


def test_config_entry_out_of_bounds() -> None:
    with pytest.raises(ConfigValueError):
        config = {"WIDTH": 5, "HEIGHT": 5, "ENTRY": (5, 5),
                  "EXIT": (4, 4), "OUTPUT_FILE": "maze_txt", "PERFECT": True}
        MazeGenerator(config)

    with pytest.raises(ConfigValueError):
        config = {"WIDTH": 5, "HEIGHT": 5, "ENTRY": (-1, -1),
                  "EXIT": (4, 4), "OUTPUT_FILE": "maze_txt", "PERFECT": True}
        MazeGenerator(config)


def test_config_exit_out_of_bounds() -> None:
    with pytest.raises(ConfigValueError):
        config = {"WIDTH": 5, "HEIGHT": 5, "ENTRY": (2, 2),
                  "EXIT": (9, 9), "OUTPUT_FILE": "maze_txt", "PERFECT": True}
        MazeGenerator(config)

    with pytest.raises(ConfigValueError):
        config = {"WIDTH": 5, "HEIGHT": 5, "ENTRY": (2, 2),
                  "EXIT": (-1, -1), "OUTPUT_FILE": "maze_txt", "PERFECT": True}
        MazeGenerator(config)
