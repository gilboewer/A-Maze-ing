from mazegen import MazeGenerator
from loadconfig import load_config
from errors import ConfigValueError, ConfigError
import pytest


def test_config_loads_correctly():
    config = load_config()
    MazeGenerator(config)


def test_config_targets_out_of_bounds():
    with pytest.raises(ConfigValueError):
        config = {"WIDTH": 5, "HEIGHT": 5, "ENTRY": (5, 5), "EXIT": (4, 4), "OUTPUT_FILE": "maze_txt", "PERFECT": True}
        MazeGenerator(config)

    with pytest.raises(ConfigValueError):
        config = {"WIDTH": 5, "HEIGHT": 5, "ENTRY": (-1, -1), "EXIT": (4, 4), "OUTPUT_FILE": "maze_txt", "PERFECT": True}
        MazeGenerator(config)

    with pytest.raises(ConfigValueError):
        config = {"WIDTH": 5, "HEIGHT": 5, "ENTRY": (2, 2), "EXIT": (9, 9), "OUTPUT_FILE": "maze_txt", "PERFECT": True}
        MazeGenerator(config)

    with pytest.raises(ConfigValueError):
        config = {"WIDTH": 5, "HEIGHT": 5, "ENTRY": (2, 2), "EXIT": (-1, -1), "OUTPUT_FILE": "maze_txt", "PERFECT": True}
        MazeGenerator(config)
