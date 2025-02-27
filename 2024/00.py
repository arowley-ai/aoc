import aocd
import martens as mt


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
puzzle = aocd.models.Puzzle(day=day, year=year)
puzzle_input_data = aocd.get_data(day=day, year=year)

example_input = puzzle.examples[0].input_data
print(example_input)

# part_a_example = part_a(example_input)
# print(part_a_example)

# part_a_answer = part_a(puzzle_input_data)
# print(part_a_answer)
#
# part_b_example = part_b(example_input)
# print(part_b_example)
#
# part_b_answer = part_b(puzzle_input_data)
# print(part_b_answer)
