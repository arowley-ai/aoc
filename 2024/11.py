import aocd
import aocar
import martens as mt


def parse_data(input_data):
    return [x for x in aocar.list_of_numbers(input_data)]


def blink(rock):
    if rock == 0:
        return [1]
    elif len(str(rock)) % 2 == 0:
        return [int(''.join(rslt)) for rslt in zip(*[(str(rock)[k], str(rock)[k + len(str(rock)) // 2]) for k in range(0, len(str(rock)) // 2)])]
    else:
        return [rock * 2024]


def solve(input_data, blinks=25):
    rocks = parse_data(input_data)
    data = mt.Dataset({'rock': rocks, 'count': [1] * len(rocks)})
    for k in range(blinks):
        data = data.mutate_stack(blink) \
            .group_by(grouping_cols=['blink'], other_cols=['count']) \
            .replace(sum, ['count']) \
            .rename_and_select({'blink': 'rock', 'count': 'count'})
    return sum(data['count'])


day, year = aocd.get_day_and_year()
puzzle = aocd.models.Puzzle(day=day, year=year)
puzzle_input_data = aocd.get_data(day=day, year=year)

example_input = "125 17"

part_a_example = solve(example_input)
print(part_a_example)

part_a_answer = solve(puzzle_input_data)
print(part_a_answer)

part_b_example = solve(example_input, blinks=75)
print(part_b_example)

part_b_example = solve(puzzle_input_data, blinks=75)
print(part_b_example)
