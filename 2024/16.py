import aocd
import martens as mt

move_grid = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
turn_grid = {'^': ('>', '<'), '>': ('v', '^'), 'v': ('<', '>'), '<': ('^', 'v')}
adjacency_generator = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def add(location, direction):
    return (location[0] + direction[0], location[1] + direction[1])


def parse_data(input_data):
    data = mt.Dataset({'line': [x for x in input_data.split('\n')]}) \
        .with_id('row_id') \
        .column_stack('line', enumeration='column_id') \
        .rename({'line': 'value'}) \
        .mutate(lambda row_id, column_id: (row_id, column_id), 'coord') \
        .filter(lambda value: value != '#') \
        .drop(['row_id', 'column_id'])
    return data


def get_paths(dirc, cost, all_coords):
    rtn = [[dirc, cost]]
    rtn.extend([[(dirc[0], dirc[1], t), cost + 1000] for t in turn_grid[dirc[2]] if add(dirc[0:2], move_grid[t]) in all_coords])
    direction = move_grid[dirc[2]]
    new_coord = (dirc[0] + direction[0], dirc[1] + direction[1], dirc[2])
    if new_coord[0:2] in all_coords:
        rtn.append([(dirc[0] + direction[0], dirc[1] + direction[1], dirc[2]), cost + 1])
    return rtn


def part_a(input_data):
    data = parse_data(input_data)
    start = data.filter('S', 'value')['coord'][0]
    end = data.filter('E', 'value')['coord'][0]
    path = mt.Dataset({'dirc': [(start[0], start[1], '>')]}).with_constants({'cost': 0})
    sum_cost = -1
    iterations = 0
    all_coords = data['coord']
    all_dircs = [(x,y,m) for x,y in all_coords for m in move_grid if add((x,y), move_grid[m]) in all_coords]
    while sum_cost != sum(path['cost']):
        iterations += 1
        sum_cost = sum(path['cost'])
        path = path.mutate_stack(lambda dirc, cost: get_paths(dirc, cost, all_coords), name='path_cost') \
            .mutate_stretch(lambda path_cost: list(path_cost), ['dirc', 'cost']).drop(['path_cost']) \
            .group_by(grouping_cols=['dirc'], other_cols=['cost']) \
            .replace(min, ['cost'])
        if iterations % 10 == 0:
            print(path.record_length / len(all_dircs))
    return min(path.filter(lambda dirc: dirc[0:2] == end)['cost'])


def get_paths_hist(dirc, cost, hist, all_coords):
    rtn = [[(dirc[0], dirc[1], t), cost + 1000] for t in turn_grid[dirc[2]] if add(dirc[0:2], move_grid[t]) in all_coords]
    direction = move_grid[dirc[2]]
    new_coord = (dirc[0] + direction[0], dirc[1] + direction[1], dirc[2])
    if new_coord[0:2] in all_coords:
        rtn.append([(dirc[0] + direction[0], dirc[1] + direction[1], dirc[2]), cost + 1])
    return [[dirc, cost, hist]] + [[dirc, cost, hist + [dirc]] for dirc, cost in rtn]


def part_b(input_data):
    data = parse_data(input_data)
    start = data.filter('S', 'value')['coord'][0]
    end = data.filter('E', 'value')['coord'][0]
    init = [(start[0], start[1], '>')]
    path = mt.Dataset({'dirc': init, 'hist': [init], 'cost': [0]})
    new_cost,sum_cost = 0,1
    all_coords = data['coord']
    iterations = 0
    while sum_cost != new_cost:
        sum_cost = new_cost
        all_paths = path.mutate_stack(lambda dirc, cost, hist: get_paths_hist(dirc, cost, hist, all_coords), name='path_cost') \
            .mutate_stretch(lambda path_cost: list(path_cost), ['dirc', 'cost', 'hist']).drop(['path_cost'])
        min_cost_path = all_paths.group_by(grouping_cols=['dirc'], other_cols=['cost']) \
            .replace(min, ['cost']).rename({'cost': 'min_cost'})
        path = all_paths.merge(min_cost_path, how='inner', on=['dirc']) \
            .filter(lambda cost, min_cost: cost == min_cost) \
            .group_by(['dirc', 'cost', 'hist'], other_cols=[])
        new_cost = sum(path['cost'])
        iterations += 1
        if iterations % 10 == 0:
            print(path.record_length / len(all_coords) / 4)
    min_cost_end = min(path.filter(lambda dirc: dirc[0:2] == end)['cost'])
    best_paths = path.filter(lambda dirc: dirc[0:2] == end).filter(lambda cost: cost==min_cost_end)['hist']
    return len({dirc[0:2] for path in best_paths for dirc in path})


day, year = aocd.get_day_and_year()
puzzle = aocd.models.Puzzle(day=day, year=year)
puzzle_input_data = aocd.get_data(day=day, year=year)

example_input = puzzle.examples[0].input_data
# print(example_input)

part_a_example = part_a(example_input)
print(part_a_example)

part_a_answer = part_a(puzzle_input_data)
print(part_a_answer)

part_b_example = part_b(example_input)
print(part_b_example)

part_b_answer = part_b(puzzle_input_data)
print(part_b_answer)
