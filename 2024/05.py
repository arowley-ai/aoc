import aocd
import martens as mt


def parse_data(input_data):
    rules_lines, manuals_lines = input_data.split('\n\n')
    manuals = mt.Dataset({'line': manuals_lines.split('\n')}) \
        .with_id('row_id').mutate(lambda line: [int(v) for v in line.split(',')], 'line') \
        .column_stack('line', new_name='value', enumeration='column_id', save_len='row_len')
    rules = mt.Dataset({'line': rules_lines.split('\n')})
    return manuals, rules


def part_a(input_data):
    manuals, rules = parse_data(input_data)
    rules_after = rules.mutate_stretch(lambda line: [int(v) for v in line.split('|')], names=['value', 'after']) \
        .group_by(grouping_cols=['value'], other_cols=['after'])
    data = manuals.rolling_mutate(lambda value: list(value)[:-1], grouping_cols=['row_id'], name='before') \
        .merge(rules_after, how='left', on=['value']).fill_none([]) \
        .mutate(lambda before, after: any(a in before for a in after), 'rule_broken') \
        .group_by(grouping_cols=['row_id'], other_cols=['rule_broken']).replace(any, ['rule_broken']) \
        .filter(False, 'rule_broken') \
        .merge(manuals.filter(lambda row_len, column_id: row_len - 1 == column_id * 2), how='inner', on=['row_id'])
    return sum(data['value']), data['row_id']


def get_correct_order(values, rules_before):
    rtn = []
    remaining_values = values
    while len(remaining_values) > 0:
        for value in remaining_values:
            if value not in rules_before or all(c in rtn or c not in remaining_values for c in rules_before[value]):
                rtn.append(value)
                remaining_values.remove(value)
                break
    return rtn


def part_b(input_data, correct_ids):
    manuals, rules = parse_data(input_data)
    wrong = manuals.filter(lambda row_id: row_id not in correct_ids).group_by(['row_id'], ['value'])
    rules_before_data = rules.mutate_stretch(lambda line: [int(v) for v in line.split('|')], names=['before', 'value']) \
        .group_by(grouping_cols=['value'], other_cols=['before'])
    rules_before = {value: tuple(before) for value, before in rules_before_data.generator(['value', 'before'])}
    fixed = wrong.mutate(lambda value: get_correct_order(value, rules_before), 'value') \
        .mutate(lambda value: value[int((len(value) + 1) / 2) - 1], 'middle')
    return sum(fixed['middle'])


day, year = aocd.get_day_and_year()
puzzle = aocd.models.Puzzle(day=day, year=year)
puzzle_input_data = aocd.get_data(day=day, year=year)

example_input = puzzle.examples[0].input_data

part_a_example, correct_ids = part_a(example_input)
print(part_a_example)

part_b_example = part_b(example_input, correct_ids)
print(part_b_example)

part_a_answer, correct_ids = part_a(puzzle_input_data)
print(part_a_answer)

part_b_answer = part_b(puzzle_input_data, correct_ids)
print(part_b_answer)
