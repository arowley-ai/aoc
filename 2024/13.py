import aocd
import martens as mt
import re
import numpy as np

regex = r'[XY][\+=](\d+)'


def validate_solution(button_a, button_b, solve):
    return [
        button_a[0] * solve[0] + button_b[0] * solve[1],
        button_a[1] * solve[0] + button_b[1] * solve[1]
    ]


def solve(button_a, button_b, prize):
    matrix = np.array([[button_a[0], button_b[0]], [button_a[1], button_b[1]]])
    z = np.linalg.solve(matrix, np.array(prize))
    if np.allclose(z, np.round(z), atol=1e-5):
        return list(np.round(z).astype(int))


def parse_data(input_data):
    lines_raw = input_data.split('\n')
    names = ['button_a', 'button_b', 'prize']
    data = mt.Dataset({'lines': [lines_raw[i:i + 3] for i in range(0, len(lines_raw), 4)]}) \
        .mutate_stretch(lambda lines: list(lines), names) \
        .drop(['lines']).replace(lambda val: val.split(': ')[1], names) \
        .replace(lambda input: re.findall(regex, input), names) \
        .replace(lambda input: [int(input[0]), int(input[1])], names)
    return data


def part_a(input_data):
    data = parse_data(input_data).mutate(solve) \
        .filter(lambda solve: solve is not None) \
        .mutate(lambda solve: 3 * solve[0] + solve[1], 'cost')
    return sum(data['cost'])


def part_b(input_data):
    data = parse_data(input_data) \
        .mutate(lambda prize: [prize[0] + 10000000000000, prize[1] + 10000000000000], 'prize') \
        .mutate(solve, 'solve') \
        .filter(lambda solve: solve is not None) \
        .mutate(validate_solution) \
        .filter(lambda prize, validate_solution: prize == validate_solution) \
        .mutate(lambda solve: 3 * solve[0] + solve[1], 'cost')
    return sum(data['cost'])


day, year = aocd.get_day_and_year()
puzzle = aocd.models.Puzzle(day=day, year=year)
puzzle_input_data = aocd.get_data(day=day, year=year)

example_input = puzzle.examples[0].input_data

part_a_example = part_a(example_input)
print(part_a_example)

part_a_answer = part_a(puzzle_input_data)
print(part_a_answer)

part_b_example = part_b(example_input)
print(part_b_example)

part_b_answer = part_b(puzzle_input_data)
print(part_b_answer)
