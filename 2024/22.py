import aocd
import martens as mt


def parse_data(input_data):
    data = mt.Dataset({'secret_number': [int(x) for x in input_data.split('\n')]}).with_id('row_id')
    return data


def get_secret_number(secret_number):
    step1_result = (secret_number * 64) % 16777216
    secret_number ^= step1_result
    secret_number %= 16777216
    step2_result = (secret_number // 32) % 16777216
    secret_number ^= step2_result
    secret_number %= 16777216
    step3_result = (secret_number * 2048) % 16777216
    secret_number ^= step3_result
    secret_number %= 16777216
    return secret_number


def part_a(input_data):
    data = parse_data(input_data)
    for k in range(2000):
        data = data.mutate(get_secret_number, 'secret_number')
    return sum(data['secret_number'])


def all_secret_numbers(secret_number):
    rtn = [secret_number]
    for k in range(2000):
        rtn.append(get_secret_number(rtn[-1]))
    return rtn


def part_b(input_data):
    data = parse_data(input_data) \
        .with_id('buyer_id') \
        .mutate_stack(all_secret_numbers, enumeration='number_id', name='number') \
        .mutate(lambda number: number % 10, 'price') \
        .rolling_mutate(lambda price: price[-2] - price[-1] if len(price) > 1 else None, name='price_change', grouping_cols=['buyer_id']) \
        .rolling_mutate(lambda price_change: tuple(price_change[-4:]), name='trigger', grouping_cols=['buyer_id']) \
        .rolling_mutate(lambda trigger: trigger[-1] if trigger[-1] not in trigger[:-1] else None, grouping_cols=['buyer_id'], name='trigger_first') \
        .filter(lambda trigger_first: trigger_first is not None and None not in trigger_first) \
        .group_by(grouping_cols=['trigger_first'], other_cols=['price']).replace(sum, ['price']).sort(['price'])
    return data['price'][-1]


day, year = aocd.get_day_and_year()
puzzle = aocd.models.Puzzle(day=day, year=year)
puzzle_input_data = aocd.get_data(day=day, year=year)

example_input = """1
10
100
2024"""

part_b_input = """1
2
3
2024"""

part_a_example = part_a(example_input)
print(part_a_example)

part_a_answer = part_a(puzzle_input_data)
print(part_a_answer)

part_b_example = part_b(part_b_input)
print(part_b_example)

part_b_answer = part_b(puzzle_input_data)
print(part_b_answer)
