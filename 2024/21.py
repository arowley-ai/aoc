from itertools import product

import aocd
import martens as mt

nkey = {
    (0, 0): '7', (0, 1): '8', (0, 2): '9',
    (1, 0): '4', (1, 1): '5', (1, 2): '6',
    (2, 0): '1', (2, 1): '2', (2, 2): '3',
    (3, 1): '0', (3, 2): 'A'
}
nkey_rvs = {nkey[k]: k for k in nkey}
nstart = next(k for k in nkey if nkey[k] == 'A')

dkey = {
    (0, 1): '^', (0, 2): 'A',
    (1, 0): '<', (1, 1): 'v', (1, 2): '>'
}
dstart = next(k for k in dkey if dkey[k] == 'A')
dkey_rvs = {dkey[k]: k for k in dkey}

move_grid = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
move_grid_rvs = {move_grid[m]: m for m in move_grid}
move_list = ['^', '<', 'v', '>', 'A']
moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]


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


def non_repeats(inputs):
    return sum(1 for a, b in zip(inputs[1:], inputs[:-1]) if a != b)


def sorting_indice(inputs):
    sort_grid = {'^': 1, '>': 1, 'A': 2, '<': 0, 'v': 0}
    return [sort_grid[code] for code in inputs]


def sort_string_by_indices(s):
    indices = {'^': 1, '>': 1, 'A': 2, '<': 0, 'v': 0}
    return ''.join(sorted(s, key=lambda x: indices[x]))


def instruction_length(line, stretch=chain):
    data = mt.Dataset(dict(line=[line], outputs=[''])).with_constant(move_grid, name='inputs').column_stack('inputs')
    while data.filter(lambda line, outputs: line == outputs).record_length == 0:
        data = data.mutate_stack(lambda inputs: [inputs + m for m in move_list], 'inputs') \
            .mutate_stretch(stretch, names=['bad_path', 'outputs']) \
            .filter(lambda line, bad_path, outputs: not bad_path and line.startswith(outputs))
    data = data.filter(lambda line, outputs: line == outputs) \
        .mutate(next_path_len).mutate(sorting_indice).mutate(non_repeats).sort(['next_path_len', 'non_repeats', 'sorting_indice'])['inputs']
    return min(next_path_len(l) for l in data)


def part_a(input_data):
    data = parse_data(input_data) \
        .mutate(lambda line: instruction_length(line), 'length') \
        .mutate(lambda line, length: length * int(line[0:3]), 'complexity')
    return sum(data['complexity'])


def expand_all_paths(path, all_paths_map):
    rtn = [all_paths_map[start][end] for start, end in zip('A' + path[:-1], path)]
    return [''.join(combination) for combination in product(*rtn)]


def tie_break_paths(paths, all_paths_map):
    path_data = mt.Dataset(dict(original=paths, inputs=paths))
    while True:
        summary = path_data.mutate(next_path_len) \
            .group_by(['original'], ['next_path_len']) \
            .replace(min, ['next_path_len'])
        min_path = min(summary['next_path_len'])
        if summary.filter(min_path, 'next_path_len').record_length == 1:
            return summary.filter(min_path, 'next_path_len')['original'][0]
        else:
            originals = summary.filter(min_path, 'next_path_len')['original']
            path_data = path_data.filter(lambda original: original in originals) \
                .mutate_stack(lambda inputs: expand_all_paths(inputs, all_paths_map), 'inputs')


def get_all_paths(start, end, pos_map, key_map):
    start_pos, end_pos = pos_map[start], pos_map[end]
    data = mt.Dataset(dict(start=[start_pos], coord=[start_pos], inputs=['']))
    while end_pos not in data['coord']:
        data = data \
            .mutate_stack(lambda coord: [m for m in moves if add(coord, m) in key_map], 'move') \
            .mutate(lambda inputs, move: inputs + move_grid_rvs[move], 'inputs') \
            .mutate(lambda coord, move: add(coord, move), 'coord') \
            .drop(['move'])
    return data.mutate(lambda inputs: inputs + 'A', 'inputs') \
        .filter(end_pos, 'coord').rename(dict(coord='end'))['inputs']


def expand_best_path(path, best_paths_map):
    return ''.join([best_paths_map[p][q] for p, q in zip('A' + path[:-1], path)])


def part_b(input_data):
    dkey_data = mt.Dataset(dict(start=list(dkey_rvs))) \
        .with_constant(list(dkey_rvs), 'end') \
        .column_stack('end') \
        .mutate(lambda start, end: get_all_paths(start, end, dkey_rvs, dkey), 'all_paths')
    nkey_data = mt.Dataset(dict(start=list(nkey_rvs))) \
        .with_constant(list(nkey_rvs), 'end') \
        .column_stack('end') \
        .mutate(lambda start, end: get_all_paths(start, end, nkey_rvs, nkey), 'all_paths')
    all_key_data = mt.stack([dkey_data, nkey_data])
    all_paths_map = {start: {e: a for e, a in zip(end, all_paths)}
                     for start, end, all_paths in
                     all_key_data.group_by(['start'], ['end', 'all_paths']).generator(['start', 'end', 'all_paths'])}
    best_paths = all_key_data \
        .mutate(lambda all_paths: tie_break_paths(all_paths, all_paths_map), 'best_path').drop(['all_paths'])
    best_paths_map = {start: {e: a for e, a in zip(end, best_path)}
                      for start, end, best_path in
                      best_paths.group_by(['start'], ['end', 'best_path']).generator(['start', 'end', 'best_path'])}
    data = parse_data(input_data).mutate(lambda line: line, 'inputs').with_constants(dict(count=1))
    for k in range(25):
        data = data.mutate(lambda inputs: [(s, e) for s, e in zip('A' + inputs[:-1], inputs)], 'inputs') \
            .column_stack('inputs').mutate_stretch(lambda inputs: list(inputs), ['start', 'end']) \
            .group_by(['line', 'start', 'end'], other_cols=['count']) \
            .replace(sum, ['count']) \
            .mutate(lambda start, end: best_paths_map[start][end], 'inputs').select(['line', 'inputs', 'count'])
    data = data.mutate(lambda line, inputs, count: count * next_path_len(inputs) * int(line[0:3]), 'complexity')
    return sum(data['complexity'])


day, year = aocd.get_day_and_year()
puzzle = aocd.models.Puzzle(day=day, year=year)
puzzle_input_data = aocd.get_data(day=day, year=year)

example_input = """029A
980A
179A
456A
379A"""

part_a_example = part_a(example_input)
print(part_a_example)

part_a_answer = part_a(puzzle_input_data)
print(part_a_answer)

part_b_example = part_b(example_input)
print(part_b_example)

part_b_answer = part_b(puzzle_input_data)
print(part_b_answer)
