#!/usr/bin/env python3
import sys
import argparse
from collections import Counter
from typing import TextIO
from datetime import datetime


def day1(input_file: TextIO) -> None:
    left_list = []
    right_list = []
    for line in input_file:
        left_n, right_n = line.strip().split()
        left_list.append(int(left_n))
        right_list.append(int(right_n))

    left_list.sort()
    right_list.sort()

    total_distance = sum(abs(l - r) for l, r in zip(left_list, right_list))
    print("total distance:", total_distance)

    right_list_counter = Counter(right_list)
    total_similarity_score = sum(n * right_list_counter[n] for n in left_list)
    print("total similarity score:", total_similarity_score)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code Solution",
        epilog="Learn more at https://adventofcode.com/",
    )
    parser.add_argument(
        "input",
        nargs="?",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="The input file (defaults to stdin if not provided)",
        metavar="FILE",
    )
    parser.add_argument(
        "--day",
        type=int,
        choices=range(1, 26),
        help="Specify a day (1-25).",
        default=datetime.now().day,
        metavar="DAY",
    )

    args = parser.parse_args()

    if fn := globals().get(f"day{args.day}"):
        fn(args.input)
    else:
        print(f"Day {args.day} not yet implemented")
        sys.exit(1)
