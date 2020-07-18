# coding: utf-8

from .hra import hra


def main():
    try:
        hra()
    except (SystemExit, EOFError, KeyboardInterrupt):
        print('\nHra končí.')


if __name__ == '__main__':
    main()
