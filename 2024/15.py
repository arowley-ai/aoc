import aocd
import martens as mt
from collections import namedtuple

move_grid = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1),
    '\x1b[A': (-1, 0),
    '\x1b[C': (0, 1),
    '\x1b[B': (1, 0),
    '\x1b[D': (0, -1)
}
replace_grid = {'#': '##', 'O': '[]', '.': '..', '@': '@.'}


def add(location, direction):
    return (location[0] + direction[0], location[1] + direction[1])


def gps_coordinate(location):
    return location[0] * 100 + location[1]


def parse_data(input_data, replace_map):
    data = mt.Dataset({'line': [x for x in input_data.split('\n')]}) \
        .with_id('row_id')
    middle_line = data.filter(lambda line: len(line) == 0)['row_id'][0]
    warehouse = data.filter(lambda row_id: row_id < middle_line) \
        .mutate(lambda line: line if replace_map is None else ''.join(replace_map[l] for l in line), 'line') \
        .column_stack('line', new_name='value', enumeration='col_id', save_len='grid_size') \
        .drop(['line']) \
        .mutate(lambda row_id, col_id: (row_id, col_id), 'lookup')
    instructions = ''.join(data.filter(lambda row_id: row_id > middle_line)['line'])
    robot = warehouse.filter('@', 'value')['lookup'][0]
    warehouse_map = {lookup: value for lookup, value in warehouse.generator(['lookup', 'value'])}
    return warehouse_map, instructions, robot, max(warehouse['row_id']) + 1, max(warehouse['col_id']) + 1


def part_a(input_data, replace_map):
    warehouse_map, instructions, robot, height, width = parse_data(input_data, replace_map)
    for instruction in instructions:
        direction = move_grid[instruction]
        new_locations = [add(robot, direction)]
        while warehouse_map[new_locations[-1]] == 'O':
            new_locations.append(add(new_locations[-1], direction))
        if warehouse_map[new_locations[-1]] == '.':
            previous = '@'
            warehouse_map[robot] = '.'
            for location in new_locations:
                current = warehouse_map[location]
                warehouse_map[location] = previous
                previous = current
            robot = new_locations[0]
    return sum(gps_coordinate(k) for k in warehouse_map if warehouse_map[k] == 'O')


class Force:
    x: int
    y: int
    moving: bool
    moved: bool


class Point(namedtuple('Point', ['coord', 'move_out'])):

    def value(self, warehouse_map):
        return warehouse_map[self.coord]

    def next(self, direction):
        return add(self.coord, direction)


def coords(points):
    return [p.coord for p in points]


def do_movement(robot, instruction, warehouse_map):
    moved = False
    direction = move_grid[instruction]
    if direction in [(0, 1), (0, -1)]:
        new_locations = [add(robot, direction)]
        while warehouse_map[new_locations[-1]] in ['[', ']']:
            new_locations.append(add(new_locations[-1], direction))
        if warehouse_map[new_locations[-1]] == '.':
            previous = '@'
            warehouse_map[robot] = '.'
            for location in new_locations:
                current = warehouse_map[location]
                warehouse_map[location] = previous
                previous = current
            robot = new_locations[0]
            moved = True
    else:
        points = [Point(robot, True)]
        moved = True
        point_added = True
        while point_added:
            point_added = False
            if any(warehouse_map[p.next(direction)] == '#' and p.move_out for p in points):
                moved = False
                break
            new_points = []
            for p in points:
                if p.move_out:
                    if p.next(direction) not in coords(points):
                        new_points.append(Point(p.next(direction), warehouse_map[p.next(direction)] != '.'))
                        point_added = True
            for p in points:
                if p.move_out:
                    if p.value(warehouse_map) == ']' and p.next((0, -1)) not in coords(points):
                        new_points.append(Point(p.next((0, -1)), True))
                        point_added = True
                    elif p.value(warehouse_map) == '[' and p.next((0, 1)) not in coords(points):
                        new_points.append(Point(p.next((0, 1)), True))
                        point_added = True
            points.extend(new_points)
        if moved:
            change_map = {p.next(direction): p.value(warehouse_map) for p in points if p.move_out}
            change_map.update({p.coord: '.' for p in points if p.move_out and p.coord not in change_map})
            for change in change_map:
                warehouse_map[change] = change_map[change]
            robot = add(robot, direction)
    return moved, robot, warehouse_map


def part_b(input_data, replace_map):
    warehouse_map, instructions, robot, height, width = parse_data(input_data, replace_map)
    for instruction in instructions:
        moved, robot, warehouse_map = do_movement(robot, instruction, warehouse_map)
    return sum(gps_coordinate(k) for k in warehouse_map if warehouse_map[k] == '[')


day, year = aocd.get_day_and_year()
puzzle = aocd.models.Puzzle(day=day, year=year)
puzzle_input_data = aocd.get_data(day=day, year=year)

example_input = puzzle.examples[0].input_data

part_a_example = part_a(example_input, replace_map=None)
print(part_a_example)

part_a_answer = part_a(puzzle_input_data, replace_map=None)
print(part_a_answer)

part_b_example = part_b(example_input, replace_map=replace_grid)
print(part_b_example)

part_b_answer = part_b(puzzle_input_data, replace_map=replace_grid)
print(part_b_answer)

# import tty
# import termios
# import sys
# import os
#
# def print_map(warehouse_map, height, width, replace_robot=None):
#     for row_id in range(height):
#         print(''.join(
#             warehouse_map[(row_id, col_id)] if replace_robot is None or warehouse_map[(row_id, col_id)] != '@' else replace_robot for col_id in range(width)
#         ))
#
#
# def do_game(input_data, replace_map):
#     warehouse_map, instructions, robot, height, width = parse_data(input_data, replace_map)
#     print_map(warehouse_map, height, width)
#     history = []
#     while True:
#         instruction = get_key()
#         if instruction == 'q':
#             break
#         if instruction == 'u':
#             if history:
#                 robot, warehouse_map = history.pop()
#             os.system('cls' if os.name == 'nt' else 'clear')
#             print_map(warehouse_map, height, width)
#             continue
#         history.append((robot, warehouse_map.copy()))
#         os.system('cls' if os.name == 'nt' else 'clear')
#         moved, robot, warehouse_map = do_movement(robot, instruction, warehouse_map)
#         for k in range(3):
#             print(' ')
#         print_map(warehouse_map, height, width)
#
#
# def get_key():
#     fd = sys.stdin.fileno()
#     old_settings = termios.tcgetattr(fd)
#     try:
#         tty.setraw(fd)
#         key = sys.stdin.read(1)
#         if key not in ['u', 'q']:
#             key += sys.stdin.read(2)
#     finally:
#         termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#     return key

# do_game(example_input, replace_map=replace_grid)
