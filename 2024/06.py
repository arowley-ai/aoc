import aocd
import martens as mt

move_grid = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
turn_grid = {'^': '>', '>': 'v', 'v': '<', '<': '^'}


def parse_data(input_data):
    data = mt.Dataset({'line': [x for x in input_data.split('\n')]}) \
        .with_id('row_id') \
        .column_stack('line', enumeration='column_id') \
        .rename({'line': 'value'}) \
        .mutate(lambda row_id, column_id: (row_id, column_id), 'lookup')
    return {lookup: value for lookup, value in data.generator(['lookup', 'value'])}, max(data['row_id']) + 1, max(data['column_id']) + 1


def get_details(grid):
    return next((x, grid[x], move_grid[grid[x]]) for x in grid if grid[x] in move_grid)


def history_is_loop(grid):
    history = []
    is_loop = False
    location, symbol, direction = get_details(grid)
    while True:
        new_location = (location[0] + direction[0], location[1] + direction[1])
        if new_location not in grid:
            history.append((location, symbol))
            break
        elif (location, symbol) in history:
            is_loop = True
            break
        elif grid[new_location] == '.':
            history.append((location, symbol))
            grid[new_location] = symbol
            grid[location] = '.'
            location = new_location
        else:
            symbol = turn_grid[grid[location]]
            direction = move_grid[symbol]
            grid[location] = symbol
    return history, is_loop


def part_a(input_data):
    grid, height, width = parse_data(input_data)
    history, is_loop = history_is_loop(grid)
    return len(set(x[0] for x in history)), history


def part_b(input_data, all_history):
    original_grid, height, width = parse_data(input_data)
    location, _, _ = get_details(original_grid)
    part_a_history = {l for l, s in all_history if l != location}
    grids = [{**original_grid, **{dot: '#'}} for dot in part_a_history]
    results = [history_is_loop(grid) for grid in grids]
    return sum(is_loop for _, is_loop in results)


day, year = aocd.get_day_and_year()
puzzle = aocd.models.Puzzle(day=day, year=year)
puzzle_input_data = aocd.get_data(day=day, year=year)

example_input = puzzle.examples[0].input_data

part_a_example, a_history = part_a(example_input)
print(part_a_example)

part_b_example = part_b(example_input, a_history)
print(part_b_example)

part_a_answer, a_history = part_a(puzzle_input_data)
print(part_a_answer)

part_b_answer = part_b(puzzle_input_data, a_history)
print(part_b_answer)
