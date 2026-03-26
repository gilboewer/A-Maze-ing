import sys
from load_config import load_config


def main():
    config_file = "default_config.txt"
    config = load_config(config_file)
    print(config)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("Unrecoverable error occured, exeting program.", file=sys.stderr)
