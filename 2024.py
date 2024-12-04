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


def day2(input_file: TextIO) -> None:
    safe_count = 0
    safe_count2 = 0

    def is_safe(d):
        return 0 < d < 4

    def is_seq_safe(seq, allow_skipping=0):
        return is_seq_safe_(None, seq, allow_skipping)

    def is_seq_safe_(prev, seq, allow_skipping=0):
        if allow_skipping < 0:
            return False

        match seq:
            case []:
                return True
            case [_]:
                return True
            case [l0, l1]:
                return is_safe(l1 - l0) or allow_skipping > 0
            case [l0, l1, *rest]:
                if is_safe(l1 - l0):
                    return is_seq_safe_(l0, [l1, *rest], allow_skipping)
                if is_seq_safe_(prev, [l0, *rest], allow_skipping - 1):
                    return True
                if (prev is None or is_safe(l1 - prev)) and is_seq_safe_(
                    prev, [l1, *rest], allow_skipping - 1
                ):
                    return True
                return False
            case _:
                raise ValueError(f"invalid sequence: {seq}")

    for line in input_file:
        levels = line.strip().split()
        levels = [int(level) for level in levels]

        diffs = [l1 - l0 for l0, l1 in zip(levels, levels[1:])]

        increasing = sum(1 for d in diffs if d > 0)
        decreasing = sum(1 for d in diffs if d < 0)
        if decreasing > increasing:  # normalize: always increasing
            levels.reverse()
            diffs = [-d for d in diffs]

        if is_seq_safe(levels):
            safe_count += 1

        if is_seq_safe(levels, allow_skipping=1):
            safe_count2 += 1

    print("safe count:", safe_count)
    print("safe count (problem dampener):", safe_count2)


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
