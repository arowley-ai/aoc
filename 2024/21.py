import aocd
import martens as mt

nkey = {
    (0, 0): '7', (0, 1): '8', (0, 2): '9',
    (1, 0): '4', (1, 1): '5', (1, 2): '6',
    (2, 0): '1', (2, 1): '2', (2, 2): '3',
    (3, 1): '0', (3, 2): 'A'
}
nstart = next(k for k in nkey if nkey[k] == 'A')

dkey = {
    (0, 1): '^', (0, 2): 'A',
    (1, 0): '<', (1, 1): 'v', (1, 2): '>'
}
dstart = next(k for k in dkey if dkey[k] == 'A')
dkey_rvs = {dkey[k]: k for k in dkey}

move_grid = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
move_list = ['^', '<', 'v', '>', 'A']


def add(position_a, position_b):
    return (position_a[0] + position_b[0], position_a[1] + position_b[1])


def parse_data(input_data):
    return mt.Dataset(dict(line=[line for line in input_data.split('\n')]))


def evaluate(inputs, keypad, position):
    outputs = ''
    hist = {position}
    for input in inputs:
        if input == 'A':
            outputs += keypad[position]
            hist = {position}
        else:
            position = add(position, move_grid[input])
            if position not in keypad:
                return True, outputs
            if position in hist:
                return True, outputs
            hist.add(position)
    return False, outputs


def chain(inputs):
    cycle, outputs = evaluate(inputs, dkey, dstart)
    if cycle:
        return [cycle, outputs]

    cycle, outputs = evaluate(outputs, nkey, nstart)
    return [cycle, outputs]


def no_key_strokes(key_a, key_b):
    position_a, position_b = dkey_rvs[key_a], dkey_rvs[key_b]
    return abs(position_a[0] - position_b[0]) + abs(position_a[1] - position_b[1]) + 1


def next_path_len(inputs):
    return sum(no_key_strokes(a, b) for a, b in zip('A' + inputs[:-1], inputs))


def repeats(inputs):
    return sum(1 for a, b in zip(inputs[1:], inputs[:-1]) if a == b)


def instruction_length(line, stretch=chain):
    data = mt.Dataset(dict(line=[line], outputs=[''])).with_constant(move_grid, name='inputs').column_stack('inputs')
    while data.filter(lambda line, outputs: line == outputs).record_length == 0:
        data = data.mutate_stack(lambda inputs: [inputs + m for m in move_list], 'inputs') \
            .mutate_stretch(stretch, names=['bad_path', 'outputs']) \
            .filter(lambda line, bad_path, outputs: not bad_path and line.startswith(outputs))
    data = data.filter(lambda line, outputs: line == outputs).mutate(next_path_len).sort(['next_path_len'])['inputs']
    return min(next_path_len(l) for l in data), data[0], data


def part_a(input_data):
    data = parse_data(input_data) \
        .mutate(lambda line: instruction_length(line)[0], 'length') \
        .mutate(lambda line, length: length * int(line[0:3]), 'complexity')
    return sum(data['complexity'])


def simple_chain(inputs):
    cycle, outputs = evaluate(inputs, nkey, nstart)
    return [cycle, outputs]


def dkey_expand(inputs):
    # positions = [dkey_rvs[input] for input in inputs]
    zip('A' + inputs[:-1], inputs)


def key_strokes(start, end):
    start_pos, end_pos = dkey_rvs[start], dkey_rvs[end]
    p1 = ('^' if start_pos[0] > end_pos[0] else 'v') * abs(start_pos[0] - end_pos[0])
    p2 = ('<' if start_pos[1] > end_pos[1] else '>') * abs(start_pos[1] - end_pos[1])
    return p1 + p2 + 'A' if start_pos[0] == 0 else p2 + p1 + 'A'


def path_expand(inputs):
    return ''.join(key_strokes(a, b) for a, b in zip('A' + inputs[:-1], inputs))


def part_b(input_data):
    # data = parse_data(input_data) \
    #     .mutate_stack(lambda line: instruction_length(line, stretch=chain)[2], 'inputs') \
    #     .mutate(next_path_len) \
    #     .mutate(lambda line, inputs: len(inputs) * int(line[0:3]), 'complexity')
    # print(data)
    #
    data = parse_data(input_data) \
        .mutate(lambda line: instruction_length(line, stretch=chain)[1], 'inputs')

    # for k in range(23):
    #     print(f'Part {k}')
    #     data = data.mutate(path_expand, 'inputs')

    data = data.mutate(lambda line, inputs: next_path_len(inputs) * int(line[0:3]), 'complexity')
    return sum(data['complexity'])


day, year = aocd.get_day_and_year()
puzzle = aocd.models.Puzzle(day=day, year=year)
puzzle_input_data = aocd.get_data(day=day, year=year)

example_input = """029A
980A
179A
456A
379A"""

# part_a_example = part_a(example_input)
# print(part_a_example)
#
# part_a_answer = part_a(puzzle_input_data)
# print(part_a_answer)

# part_b_example = part_b(example_input)
# print(part_b_example)
#
part_b_answer = part_b(puzzle_input_data)
print(part_b_answer)
