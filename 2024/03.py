import aocd
import martens as mt
import re
import math

example_input = r"xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

pattern_one = r'(mul\(\d+,\d+\))'
pattern_two = r"(mul\(\d+,\d+\)|do\(\)|don\'t\(\))"
pattern_mul = r'^mul\((\d+),(\d+)\)$'
do, dont = "do()", "don't()"


def mul_components(matches):
    if match := re.match(pattern_mul, matches):
        return math.prod([int(match.group(1)), int(match.group(2))])
    return 0


def start_stop_command(matches):
    matches_filtered = [m for m in matches if m in [do, dont]]
    return 1 if len(matches_filtered) == 0 or matches_filtered[-1] == do else 0


def parse_data(input_data, pattern):
    data = mt.Dataset({'matches': re.findall(pattern, input_data)}) \
        .mutate(mul_components)
    return data


def part_a(input_data):
    data = parse_data(input_data, pattern_one)
    return sum(data['mul_components'])


def part_b(input_data):
    data = parse_data(input_data, pattern_two) \
        .rolling_mutate(start_stop_command) \
        .mutate(lambda start_stop_command, mul_components: start_stop_command * mul_components, 'filtered_commands')
    return sum(data['filtered_commands'])


day, year = aocd.get_day_and_year()
puzzle_input_data = aocd.get_data(day=day, year=year)

part_a_example = part_a(example_input)
print(part_a_example)

part_a_answer = part_a(puzzle_input_data)
print(part_a_answer)

part_b_example = part_b(example_input)
print(part_b_example)

part_b_answer = part_b(puzzle_input_data)
print(part_b_answer)
