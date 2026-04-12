#!/usr/bin/env python3
import sys

from loadconfig import load_config
# from mazegen import MazeGenerator


def main():
    if len(sys.argv) > 2:
        raise Exception("Program takes only 1 optional argument: config file")

    config = load_config()
    print("config: ", config)

    # mazegen = MazeGenerator(config)
    # maze = mazegen.generate()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{e.__class__.__name__}: {e}", file=sys.stderr)
        print("Exeting program.", file=sys.stderr)
        sys.exit(1)
