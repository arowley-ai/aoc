import aocd
import martens as mt
import re


def list_of_numbers(line):
    return [int(m.group()) for m in re.finditer(r'\b\d+\b', line)]


def trend(report):
    if len(report) < 2:
        return None
    elif abs(report[-1] - report[-2]) > 3:
        return 'U'
    elif report[-1] > report[-2]:
        return 'D'
    elif report[-1] < report[-2]:
        return 'I'
    else:
        return 'E'


def safe_unsafe(trend):
    if len(set(trend)) > 1:
        return 0
    elif 'U' in trend or 'E' in trend:
        return 0
    else:
        return 1


def report_expand(report_simple):
    return [[v for i, v in enumerate(report_simple) if i != n] for n in range(len(report_simple))]


def parse_data(input_data):
    return mt.Dataset({'line': [x for x in input_data.split('\n')]}).with_id('row_id')


def part_a(input_data):
    data = parse_data(input_data) \
        .mutate_stack(list_of_numbers, 'report', enumeration='column_id') \
        .select(['row_id', 'column_id', 'report']) \
        .rolling_mutate(trend, grouping_cols=['row_id']) \
        .filter(lambda column_id: column_id != 0) \
        .group_by(grouping_cols=['row_id'], other_cols=['trend']) \
        .mutate(safe_unsafe)
    return sum(data['safe_unsafe'])


def part_b(input_data):
    data = parse_data(input_data) \
        .mutate(list_of_numbers, 'report_simple') \
        .mutate_stack(report_expand, enumeration='version_id', name='report') \
        .column_stack('report', enumeration='column_id') \
        .select(['row_id', 'column_id', 'version_id', 'report']) \
        .rolling_mutate(trend, grouping_cols=['row_id', 'version_id']) \
        .filter(lambda column_id: column_id != 0) \
        .group_by(grouping_cols=['row_id', 'version_id'], other_cols=['trend']) \
        .mutate(safe_unsafe) \
        .group_by(grouping_cols=['row_id'], other_cols=['safe_unsafe']) \
        .replace(max, ['safe_unsafe'])
    return sum(data['safe_unsafe'])


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
