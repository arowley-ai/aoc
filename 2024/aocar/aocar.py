import aocd
import martens as mt
import re


def dummy(input_data):
    return None


def list_of_numbers(line):
    return [int(m.group()) for m in re.finditer(r'\b\d+\b', line)]


def print_example_table(day, year, part_a=dummy, part_b=dummy):
    puzzle = aocd.models.Puzzle(day=day, year=year)
    example_table = mt.Dataset({'example': puzzle.examples}) \
        .with_id('example_no') \
        .mutate_stretch(lambda example: list(example.answers), names=['answer_one', 'answer_two']) \
        .mutate(lambda example: example.input_data, 'input_data') \
        .mutate(part_a) \
        .mutate(part_b) \
        .drop(['example', 'input_data'])
    print(example_table)
    return
