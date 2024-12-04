import aocd
import martens as mt
import aocar

example_input = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

offsets = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, -1), (-1, 1), (1, 1), (-1, -1)]
xmas = ('X', 'M', 'A', 'S')
offsets_b = [(0, 0), (-1, -1), (1, 1), (-1, 1), (1, -1)]
dirs = ['C', 'TL', 'BR', 'TR', 'BL']


def data_copy_offset(data, multiplier):
    return data.with_constant(offsets, 'offset') \
        .column_stack('offset') \
        .mutate(lambda row_id, offset: row_id - offset[0] * multiplier, 'row_id') \
        .mutate(lambda column_id, offset: column_id - offset[1] * multiplier, 'column_id') \
        .rename({'value': xmas[multiplier]})


def data_copy_offset_b(data, index):
    return data.with_constant(offsets_b[index], 'offset') \
        .mutate(lambda row_id, offset: row_id - offset[0], 'row_id') \
        .mutate(lambda column_id, offset: column_id - offset[1], 'column_id') \
        .drop(['offset']).rename({'value': dirs[index]})


def parse_data(input_data):
    return mt.Dataset({'line': [x for x in input_data.split('\n')]}) \
        .with_id('row_id') \
        .column_stack('line', enumeration='column_id') \
        .rename({'line': 'value'})


def part_a(input_data):
    data_raw = parse_data(input_data)
    data = data_copy_offset(data_raw, 0)
    for index in range(1, 4):
        data = data.merge(data_copy_offset(data_raw, index), how='inner', on=['row_id', 'column_id', 'offset'])
    data = data.filter(
        lambda X, M, A, S: X == 'X' and M == 'M' and A == 'A' and S == 'S'
    )
    return data.record_length


def part_b(input_data):
    data_raw = parse_data(input_data)
    data = data_copy_offset_b(data_raw, 0)
    for index in range(1, 5):
        data = data.merge(data_copy_offset_b(data_raw, index), how='inner', on=['row_id', 'column_id'])
    return data.filter('A', 'C') \
        .mutate(lambda TL, BR, TR, BL: TL + BR + TR + BL, 'MMSS') \
        .filter(lambda MMSS: MMSS.count('S') == 2 and MMSS.count('M') == 2 and MMSS[0] != MMSS[1]) \
        .record_length



day, year = aocd.get_day_and_year()
puzzle_input_data = aocd.get_data(day=day, year=year)

part_a_example = part_a(example_input)
print(part_a_example)

part_a_answer = part_a(puzzle_input_data)
print(part_a_answer)

part_b_example = part_b(example_input)
print(part_b_example)

part_b_answer = part_b(puzzle_input_data)
print(part_b_answer)
