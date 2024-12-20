import aocd
import martens as mt
import re

directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def add(location, direction):
    return (location[0] + direction[0], location[1] + direction[1])


def two_away(coord):
    offsets = [(2, 0), (-2, 0), (0, 2), (0, -2), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    return [add(coord, offset) for offset in offsets]


def twenty_away(coord, all_coords, distance=20):
    x, y = coord
    return [
        (x + dx, y + dy, abs(dx)+abs(dy))
        for dx in range(-distance, distance + 1)
        for dy in range(-distance, distance + 1)
        if abs(dx) + abs(dy) <= distance
        and (x + dx, y + dy) in all_coords
    ]


def tuple_of_numbers(line):
    return tuple(int(m.group()) for m in re.finditer(r'\b\d+\b', line))


def parse_data(input_data):
    data = mt.Dataset({'line': [x for x in input_data.split('\n')]}) \
        .with_id('row_id') \
        .column_stack('line', enumeration='column_id') \
        .rename({'line': 'value'}) \
        .mutate(lambda row_id, column_id: (row_id, column_id), 'coord') \
        .filter(lambda value: value != '#') \
        .drop(['row_id', 'column_id'])
    return data


def get_paths(coord, length, all_coords):
    rtn = [[coord, length]]
    for dirc in directions:
        new_coord = add(coord, dirc)
        if new_coord in all_coords:
            rtn.append([new_coord, length + 1])
    return rtn


def part_a(input_data):
    data = parse_data(input_data)
    start = data.filter('S', 'value')['coord'][0]
    end = data.filter('E', 'value')['coord'][0]
    all_coords = set(data.filter(lambda value: value in ['.', 'S', 'E'])['coord'])
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
        if iterations % 100 == 0:
            print(path.record_length / len(all_coords))
    # print(path.sort(['length']))
    cheats = path.mutate_stack(two_away) \
        .merge(path.rename({'coord': 'two_away', 'length': 'cheat_length'}), on=['two_away'], how='inner') \
        .mutate(lambda length, cheat_length: length - cheat_length - 2, 'saved') \
        .filter(lambda saved: saved >= 100)
    # .group_by(grouping_cols=['saved'], other_cols=[],count='count')
    return cheats.record_length


def part_b(input_data):
    data = parse_data(input_data)
    start = data.filter('S', 'value')['coord'][0]
    end = data.filter('E', 'value')['coord'][0]
    all_coords = set(data.filter(lambda value: value in ['.', 'S', 'E'])['coord'])
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
        if iterations % 100 == 0:
            print(path.record_length / len(all_coords))
    cheats = path.mutate_stack(lambda coord: twenty_away(coord,all_coords), name='twenty_away') \
        .mutate_stretch(lambda twenty_away: [twenty_away[0:2], twenty_away[2]], names=['twenty_away', 'cost']) \
        .merge(path.rename({'coord': 'twenty_away', 'length': 'cheat_length'}), on=['twenty_away'], how='inner') \
        .mutate(lambda coord, length, cheat_length, cost: length - cheat_length - cost, 'saved') \
        .filter(lambda saved: saved >= 100)
    return cheats.record_length


day, year = aocd.get_day_and_year()
puzzle = aocd.models.Puzzle(day=day, year=year)
puzzle_input_data = aocd.get_data(day=day, year=year)

example_input = puzzle.examples[0].input_data
print(example_input)

part_a_example = part_a(example_input)
print(part_a_example)

part_a_answer = part_a(puzzle_input_data)
print(part_a_answer)

part_b_example = part_b(example_input)
print(part_b_example)

part_b_answer = part_b(puzzle_input_data)
print(part_b_answer)
