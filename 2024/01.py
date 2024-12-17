import aocd
import martens as mt
import re


def list_of_numbers(line):
    return [int(m.group()) for m in re.finditer(r'\b\d+\b', line)]


def parse_data(input_data):
    data = mt.Dataset({'line': [x for x in input_data.split('\n')]}) \
        .with_id('row_id') \
        .mutate_stretch(list_of_numbers, names=['first', 'second']) \
        .drop(['line']) \
        .sort(['first'])
    return data


def part_a(input_data):
    data = parse_data(input_data) \
        .long_mutate(lambda second: sorted(second), 'sorted_second') \
        .mutate(lambda first, sorted_second: abs(sorted_second - first), 'difference')
    return data.long_apply(lambda difference: sum(difference))


def part_b(input_data):
    data = parse_data(input_data) \
        .long_mutate(lambda first, second: [sum([s for s in second if s == f]) for f in first], 'second_appearing')
    return sum(data['second_appearing'])


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
