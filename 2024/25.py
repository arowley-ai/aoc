import aocd
import martens as mt


def parse_data(input_data):
    data = mt.Dataset({'line': [x for x in input_data.split('\n\n')]}) \
        .mutate(lambda line: line.split('\n')[0].count('#') == len(line.split('\n')[0]), 'is_key') \
        .mutate(lambda line: [l.count('#') - 1 for l in zip(*line.split('\n'))], 'value') \
        .drop(['line'])
    return data.filter(False, 'is_key').rename_and_select({'value': 'lock_value'}), \
        data.filter(True, 'is_key').rename_and_select({'value': 'key_value'})


def fits(lock_value, key_value):
    return all(l + k < 6 for l, k in zip(lock_value, key_value))


def part_a(input_data):
    locks, keys = parse_data(input_data)
    return sum(locks.full_outer_merge(keys).mutate(fits)['fits'])


day, year = aocd.get_day_and_year()
puzzle = aocd.models.Puzzle(day=day, year=year)
puzzle_input_data = aocd.get_data(day=day, year=year)

example_input = puzzle.examples[0].input_data
# print(example_input)

part_a_example = part_a(example_input)
print(part_a_example)

part_a_answer = part_a(puzzle_input_data)
print(part_a_answer)
