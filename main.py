#!/usr/bin/env python3

import sys
from load_config import load_config


def main():
    if len(sys.argv) > 2:
        raise Exception("Program takes only 1 argument: config file")

    config = load_config()
    print(config)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{e.__class__.__name__}: {e}", file=sys.stderr)
        print("Exeting program.", file=sys.stderr)
        sys.exit(1)
