# -*- coding: utf-8 -*-
"""Console script for chibi_dl_tmo."""
import argparse
import sys


def main():
    """Console script for chibi_dl_tmo."""
    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    args = parser.parse_args()

    print("Arguments: " + str(args._))
    print("Replace this message by putting your code into "
          "chibi_dl_tmo.cli.main")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
