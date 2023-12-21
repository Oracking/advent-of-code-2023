from typing import List
from urllib.request import Request
from urllib.request import urlopen
import os
from sample_results.results import SAMPLE_RESULTS


def run(year: int, day: int, part: int):
    day_input = load_input(year, day)
    solver = dynamically_import_name_from_module(f"part_{part}", f"solutions.day_{day}.part_{part}")
    sample_input = read_file(f"solutions/day_{day}/sample_{part}.txt")
    run_solver_against_input(solver, sample_input, SAMPLE_RESULTS[f"day_{day}"][part - 1], day_input)


def load_input(year: int, day: int) -> List[str]:
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    aoc_cookie = os.getenv("AOC_COOKIE")
    if aoc_cookie is None:
        raise EnvironmentError("Could not find environment variable 'AOC_COOKIE'. Please note this environment "
                               "variable needs to be set for code to grab input for the day")
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Cookie': f'{aoc_cookie}'})
    return [line.decode("utf-8").strip("\n") for line in urlopen(req).readlines()]


def dynamically_import_name_from_module(name: str, module: str):
    module = __import__(module, fromlist=[name])
    return getattr(module, name)


def read_file(input_file_path: str) -> List[str]:
    with open(input_file_path, "r") as input_file:
        return [line.strip("\n") for line in input_file.readlines()]


def run_solver_against_input(solver, sample_input: List[str], sample_answer: int, input_content: List[str]):
    print("=" * 100)
    print("Running sample...")
    sample_output = solver(sample_input)
    print(f"Sample produced following output: {sample_output}")
    if sample_output == sample_answer:
        print("Sample passed!\nRunning real scenario...")
        print(f"Real scenario produced: {solver(input_content)}")
    else:
        print(f"Sample failed! Expected {sample_answer} but got {sample_output}")
    print("=" * 100 + "\n")


if __name__ == "__main__":
    run(year=2023, day=20, part=2)
