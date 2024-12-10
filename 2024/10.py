import aocd
import martens as mt

adjacency_generator = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def parse_data(input_data):
    data = mt.Dataset({'line': [x for x in input_data.split('\n')]}) \
        .with_id('row_id') \
        .column_stack('line', enumeration='col_id') \
        .mutate(lambda row_id, col_id: (row_id, col_id), 'coord') \
        .replace(int, ['line']) \
        .mutate(lambda coord: [(coord[0] + a[0], coord[1] + a[1]) for a in adjacency_generator], 'adjacency')
    grid_size = max(data['col_id'] + data['row_id'])
    return data.rename({'line': 'value'}).drop(['row_id', 'column_id']), grid_size


def score(test_coord, data):
    locations = [test_coord]
    for step in range(1, 10):
        locations = data.filter(step, 'value') \
            .filter(lambda adjacency: any(location in adjacency for location in locations)) \
            .long_apply(lambda coord: list(coord))
    return len(locations)


def get_next_locations(data, step, location):
    return data.filter(step, 'value') \
        .filter(lambda adjacency: location in adjacency) \
        .long_apply(lambda coord: list(coord))


def score_b(test_coord, data):
    locations = [test_coord]
    results = mt.Dataset({'0': locations})
    for step in range(1, 10):
        results = [get_next_locations(data, step, location) for location in results[str(step - 1)]]
        results = results.column_stack(str(step))
    return results.record_length


def solve(input_data, score_function=score):
    data, grid_size = parse_data(input_data)
    scores = data.filter(0, 'value') \
        .rename({'coord': 'test_coord'}) \
        .with_constant(mt.Dataset(data), name='data') \
        .mutate(score_function)
    return sum(scores[scores.columns[-1]])


day, year = aocd.get_day_and_year()
puzzle = aocd.models.Puzzle(day=day, year=year)
puzzle_input_data = aocd.get_data(day=day, year=year)

example_input = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

part_a_example = solve(example_input)
print(part_a_example)

part_a_answer = solve(puzzle_input_data)
print(part_a_answer)

part_b_example = solve(example_input, score_function=score_b)
print(part_b_example)

part_b_example = solve(puzzle_input_data, score_function=score_b)
print(part_b_example)
