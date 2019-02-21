#!/usr/bin/env python3

import sys
from datetime import datetime as dt


def bongs(hour):
    return (["BONG!" for _ in range(0, hour)])


def main():
    if len(sys.argv) == 1:
        sys.exit("I am looking for a number.")
    elif len(sys.argv) == 2:
        hour_str = sys.argv[1]
    else:
        hour_str = dt.now().strftime('%I')

    try:
        HOUR = int(hour_str)
        if HOUR < 1:
            sys.exit("There is at least 1 hour in everyday, I am sure of it")
        elif HOUR > 12:
            sys.exit("12 hours, be it AM or PM is enough for anybody!")
        else:
            print(*bongs(HOUR), sep=" ")

    except ValueError:
        sys.exit(f"{hour_str} does not appear to be a number between 1 and 12")


if __name__ == "__main__":
    main()
