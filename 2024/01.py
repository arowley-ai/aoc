import aocd
import martens as mt
import aocar


def parse_data(input_data):
    data = mt.Dataset({'line': [x for x in input_data.split('\n')]}) \
        .with_id('row_id') \
        .mutate_stretch(aocar.list_of_numbers, names=['first', 'second']) \
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
puzzle_input_data = aocd.get_data(day=day, year=year)
aocar.print_example_table(day, year, part_a=part_a, part_b=part_b)

part_a_answer = part_a(puzzle_input_data)
print(part_a_answer)
# aocd.submit(part_a_answer, part="a", day=day, year=year)

part_b_answer = part_b(puzzle_input_data)
print(part_b_answer)
# aocd.submit(part_b_answer, part="b", day=day, year=year)
