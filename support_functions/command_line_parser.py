import sys
import argparse


def parse_command_line_params():
    parser = argparse.ArgumentParser(description="Required params")
    parser.add_argument("-c", help="class name")
    parser.add_argument("-v", help="chronicle version")
    args = parser.parse_args()
    config = vars(args)

    if config["c"] is None or config["v"] is None:
        parser.print_help()
        sys.exit()

    return config
