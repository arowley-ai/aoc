import aocd
import martens as mt
import aocar


def parse_data(input_data):
    data = mt.Dataset({'line': [x for x in input_data.split('\n')]}) \
        .with_id('row_id')
    return data


def part_a(input_data):
    data = parse_data(input_data)
    print(data)
    return None


def part_b(input_data):
    data = parse_data(input_data)
    print(data)
    return None


day, year = aocd.get_day_and_year()
puzzle_input_data = aocd.get_data(day=day, year=year)
aocar.print_example_table(day, year, part_a=part_a, part_b=part_b)

part_a_answer = part_a(puzzle_input_data)
print(part_a_answer)
# aocd.submit(part_a_answer, part="a", day=day, year=year)

part_b_answer = part_b(puzzle_input_data)
print(part_b_answer)
# aocd.submit(part_b_answer, part="b", day=day, year=year)
