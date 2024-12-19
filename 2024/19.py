import aocd


def parse_data(input_data):
    data = [x for x in input_data.split('\n')]
    towels = set(data[0].split(', '))
    flags = data[2:]
    return towels, flags, max(len(towel) for towel in towels)


def is_possible(flag, towels, max_towel_length, bad_flags):
    flag_length = len(flag)
    if flag in towels:
        return True
    for length in range(0, min(max_towel_length + 1, flag_length))[::-1]:
        if flag[0:length] in towels and flag[length:] not in bad_flags:
            if is_possible(flag[length:], towels, max_towel_length, bad_flags):
                return True
            else:
                bad_flags.add(flag[length:])
    return False


def part_a(input_data):
    towels, flags, max_towel_length = parse_data(input_data)
    return sum(is_possible(flag, towels, max_towel_length, set()) for flag in flags)


def count_methods(flag, towels, max_towel_length, computed_flags):
    flag_length = len(flag)
    rtn = 0
    if flag in towels:
        rtn = rtn + 1
    for length in range(0, min(max_towel_length + 1, flag_length)):
        if flag[0:length] in towels and flag[length:]:
            if flag[length:] in computed_flags:
                count = computed_flags[flag[length:]]
            else:
                count = count_methods(flag[length:], towels, max_towel_length, computed_flags)
                computed_flags[flag[length:]] = count
            rtn += count
    return rtn


def part_b(input_data):
    towels, flags, max_towel_length = parse_data(input_data)
    return sum(count_methods(flag, towels, max_towel_length, dict()) for flag in flags)


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
