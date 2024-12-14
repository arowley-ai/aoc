import aocd
import martens as mt
import re
from math import prod


def line_data(line):
    pattern = r"p=(-?\d+),(-?\d+)\s+v=(-?\d+),(-?\d+)"
    matches = [int(g) for g in re.match(pattern, line).groups()]
    return [(matches[0], matches[1]), (matches[2], matches[3])]


def get_rest_position(position, velocity, grid, time):
    return tuple((p + time * v) % g for p, v, g in zip(position, velocity, grid))


def in_bounds(rest, grid):
    return all(r != (g - 1) // 2 for r, g in zip(rest, grid))


def quadrant(rest, grid):
    return sum(0 if r < (g - 1) // 2 else 1 + n for r, g, n in zip(rest, grid, range(len(grid))))


def parse_data(input_data):
    data = mt.Dataset({'line': [x for x in input_data.split('\n')]}) \
        .mutate_stretch(line_data, names=['position', 'velocity']).drop(['line'])
    return data


def part_a(input_data, dimensions):
    data = parse_data(input_data) \
        .with_constants(dimensions) \
        .mutate(get_rest_position, 'rest') \
        .filter(in_bounds) \
        .mutate(quadrant) \
        .group_by(grouping_cols=['quadrant'], count='count')
    return prod(data['count'])


def print_grid(data, grid):
    for y in range(grid[0]):
        print(''.join('.' if (x, y) not in data else str(data[(x, y)]) for x in range(grid[1])))
    return


def closest(rest):
    return sum(
        min(
            (abs(p[0] - q[0]) + abs(p[1] - q[1]))
            for q in rest
            if p != q or rest.count(p) > 1  # Allow duplicates to compute zero distance
        )
        for p in rest
    )


def part_b(input_data, grid, trials, print_no):
    raw_data = parse_data(input_data) \
        .with_constant(grid, 'grid') \
        .with_constant(list(range(trials)), 'time') \
        .column_stack('time') \
        .mutate(get_rest_position, 'rest')
    agg_data = raw_data.group_by(grouping_cols=['time'], other_cols=['rest']) \
        .mutate(closest) \
        .sort(['closest'])
    for xmas in agg_data['time'][0:print_no]:
        data = raw_data.filter(xmas, 'time') \
            .group_by(grouping_cols=['rest'], count='count')
        print(f'Tree {xmas}')
        print_grid({rest: count for rest, count in data.generator(['rest', 'count'])}, grid)


day, year = aocd.get_day_and_year()
puzzle = aocd.models.Puzzle(day=day, year=year)
puzzle_input_data = aocd.get_data(day=day, year=year)

example_dimensions = {'grid': (11, 7), 'time': 100}
example_input = puzzle.examples[0].input_data
actual_dimensions = {'grid': (101, 103), 'time': 100}

part_b_answer = part_b(puzzle_input_data, grid=(101, 103), trials=10000, print_no=20)

