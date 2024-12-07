import aocd
import martens as mt
import aocar
from itertools import product


def parse_combinations(ingredients, operations):
    rtn = ingredients.pop(0)
    while len(ingredients) > 0:
        operation = operations.pop(0)
        if operation != '|':
            rtn = rtn * ingredients.pop(0) if operation == '*' else rtn + ingredients.pop(0)
        else:
            rtn = int(str(rtn)+str(ingredients.pop(0)))
    return rtn


def parse_data(input_data):
    data = mt.Dataset({'line': [x for x in input_data.split('\n')]}) \
        .with_id('row_id').mutate_stretch(lambda line: line.split(':'), ['answer', 'ingredients']) \
        .replace(aocar.list_of_numbers, ['ingredients']) \
        .replace(int, ['answer'])
    return data


def part_a(input_data):
    data = parse_data(input_data) \
        .mutate_stack(lambda ingredients: list(product('*+', repeat=len(ingredients) - 1)), 'operations') \
        .replace(list, ['ingredients', 'operations']) \
        .mutate(parse_combinations, 'evaluation') \
        .filter(lambda answer, evaluation: answer == evaluation) \
        .group_by(grouping_cols=['row_id'], other_cols=['answer']) \
        .replace(lambda answer: answer[0], ['answer'])
    return sum(data['answer'])


def part_b(input_data):
    data = parse_data(input_data) \
        .mutate_stack(lambda ingredients: list(product('*+|', repeat=len(ingredients) - 1)), 'operations') \
        .replace(list, ['ingredients', 'operations']) \
        .mutate(parse_combinations, 'evaluation') \
        .filter(lambda answer, evaluation: answer == evaluation) \
        .group_by(grouping_cols=['row_id'], other_cols=['answer']) \
        .replace(lambda answer: answer[0], ['answer'])
    return sum(data['answer'])


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
#
part_b_answer = part_b(puzzle_input_data)
print(part_b_answer)
