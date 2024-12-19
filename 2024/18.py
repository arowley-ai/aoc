import aocd
import martens as mt
import re

directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def add(location, direction):
    return (location[0] + direction[0], location[1] + direction[1])


def tuple_of_numbers(line):
    return tuple(int(m.group()) for m in re.finditer(r'\b\d+\b', line))


def parse_data(input_data):
    return [tuple_of_numbers(line) for line in input_data.split('\n')]


def get_paths(coord, length, all_coords):
    rtn = [[coord, length]]
    for dirc in directions:
        new_coord = add(coord, dirc)
        if new_coord in all_coords:
            rtn.append([new_coord, length + 1])
    return rtn


def part_a(input_data, grid_size, bytes):
    start = (0, 0)
    end = (grid_size[0] - 1, grid_size[1] - 1)
    data = parse_data(input_data)
    all_coords = [(x, y) for x in range(grid_size[0]) for y in range(grid_size[1]) if (x, y) not in data[:bytes]]
    path = mt.Dataset({'coord': [start]}).with_constants({'length': 0})
    iterations = 0
    sum_length = -1
    while sum_length != sum(path['length']):
        iterations += 1
        sum_length = sum(path['length'])
        path = path.mutate_stack(lambda coord, length: get_paths(coord, length, all_coords), name='path_length') \
            .mutate_stretch(lambda path_length: list(path_length), ['coord', 'length']).drop(['path_length']) \
            .group_by(grouping_cols=['coord'], other_cols=['length']) \
            .replace(min, ['length'])
        if iterations % 10 == 0:
            print(path.record_length / len(all_coords))
    print(path)
    return min(path.filter(end, 'coord')['length'])


def calc_path(input_data, grid_size, bytes):
    start = (0, 0)
    end = (grid_size[0] - 1, grid_size[1] - 1)
    data = parse_data(input_data)
    path = mt.Dataset({'coord': [start]}).with_constants({'length': 0})
    iterations = 0
    sum_length = -1
    while sum_length != sum(path['length']):
        iterations += 1
        sum_length = sum(path['length'])
        all_coords = [(x, y) for x in range(grid_size[0]) for y in range(grid_size[1]) if (x, y) not in data[:bytes]]
        path = path.mutate_stack(lambda coord, length: get_paths(coord, length, all_coords), name='path_length') \
            .mutate_stretch(lambda path_length: list(path_length), ['coord', 'length']).drop(['path_length']) \
            .group_by(grouping_cols=['coord'], other_cols=['length']) \
            .replace(min, ['length'])
    return end in path['coord']


def part_b(input_data, grid_size, bytes):
    start, end = bytes, len(parse_data(input_data))
    while (end-start) > 1:
        trial = (start+end)//2
        print(f'Bounds {start},{end} testing {trial}')
        result = calc_path(input_data, grid_size, trial)
        start = trial if result else start
        end = end if result else trial
    return parse_data(input_data)[start]


day, year = aocd.get_day_and_year()
puzzle = aocd.models.Puzzle(day=day, year=year)
puzzle_input_data = aocd.get_data(day=day, year=year)

example_input = puzzle.examples[0].input_data
# print(example_input)

part_a_example = part_a(example_input, grid_size=(7, 7), bytes=12)
print(part_a_example)

part_a_answer = part_a(puzzle_input_data, grid_size=(71, 71), bytes=1024)
print(part_a_answer)

part_b_example = part_b(example_input, grid_size=(7, 7), bytes=12)
print(part_b_example)

part_b_answer = part_b(puzzle_input_data, grid_size=(71, 71), bytes=1024)
print(part_b_answer)
