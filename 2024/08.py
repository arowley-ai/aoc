import aocd
import martens as mt


def antinode(coord_a, coord_b):
    return [
        (2 * coord_a[0] - coord_b[0], 2 * coord_a[1] - coord_b[1]),
        (2 * coord_b[0] - coord_a[0], 2 * coord_b[1] - coord_a[1])
    ]


def resonance(coord_a, coord_b, grid_size):
    return [(k * coord_a[0] - (k - 1) * coord_b[0], k * coord_a[1] - (k - 1) * coord_b[1]) for k in range(grid_size)] + \
        [(k * coord_b[0] - (k - 1) * coord_a[0], k * coord_b[1] - (k - 1) * coord_a[1]) for k in range(grid_size)]


def parse_data(input_data):
    data = mt.Dataset({'line': [x for x in input_data.split('\n')]}) \
        .with_id('row_id') \
        .column_stack('line', enumeration='col_id') \
        .mutate(lambda row_id, col_id: (row_id, col_id), 'coord')
    grid_size = max(data['col_id'] + data['row_id'])
    return data.rename_and_select({'coord': 'coord', 'line': 'value'}), grid_size


def part_a(input_data):
    raw_data, _ = parse_data(input_data)
    data = raw_data.filter(lambda value: value != '.') \
        .rename({'coord': 'coord_a'}) \
        .merge(raw_data.filter(lambda value: value != '.').rename({'coord': 'coord_b'}), on=['value']) \
        .filter(lambda coord_a, coord_b: coord_a != coord_b) \
        .mutate_stack(antinode)
    return len(set([a for a in data['antinode'] if a in raw_data['coord']]))


def part_b(input_data):
    raw_data, grid_size = parse_data(input_data)
    data = raw_data.filter(lambda value: value != '.') \
        .rename({'coord': 'coord_a'}) \
        .merge(raw_data.filter(lambda value: value != '.').rename({'coord': 'coord_b'}), on=['value']) \
        .filter(lambda coord_a, coord_b: coord_a != coord_b) \
        .with_constant(grid_size, 'grid_size') \
        .mutate_stack(resonance)
    return len(set([a for a in data['resonance'] if a in raw_data['coord']]))


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

part_b_example = part_b(puzzle_input_data)
print(part_b_example)
