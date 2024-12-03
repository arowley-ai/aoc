import aocar
import aocd
import martens as mt


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
    data = mt.Dataset({'line': [x for x in input_data.split('\n')]}) \
        .with_id('row_id') \
        .mutate_stack(aocar.list_of_numbers, 'report', enumeration='column_id') \
        .select(['row_id', 'column_id', 'report'])
    return data


def parse_data_two(input_data):
    data = mt.Dataset({'line': [x for x in input_data.split('\n')]}) \
        .with_id('row_id') \
        .mutate(aocar.list_of_numbers, 'report_simple') \
        .mutate_stack(report_expand, enumeration='version_id', name='report') \
        .column_stack('report', enumeration='column_id') \
        .select(['row_id', 'column_id', 'version_id', 'report'])
    return data


def part_a(input_data):
    data = parse_data(input_data) \
        .rolling_mutate(trend, grouping_cols=['row_id']) \
        .filter(lambda column_id: column_id != 0) \
        .group_by(grouping_cols=['row_id'], other_cols=['trend']) \
        .mutate(safe_unsafe)
    return sum(data['safe_unsafe'])


def part_b(input_data):
    data = parse_data_two(input_data) \
        .rolling_mutate(trend, grouping_cols=['row_id', 'version_id']) \
        .filter(lambda column_id: column_id != 0) \
        .group_by(grouping_cols=['row_id', 'version_id'], other_cols=['trend']) \
        .mutate(safe_unsafe) \
        .group_by(grouping_cols=['row_id'], other_cols=['safe_unsafe']) \
        .mutate(lambda safe_unsafe: max(safe_unsafe), 'safe_unsafe')
    return sum(data['safe_unsafe'])

day, year = aocd.get_day_and_year()
puzzle_input_data = aocd.get_data(day=day, year=year)
aocar.print_example_table(day, year, part_a=part_a, part_b=part_b)

part_a_answer = part_a(puzzle_input_data)
print(part_a_answer)

part_b_answer = part_b(puzzle_input_data)
print(part_b_answer)