import aocd
import networkx as nx


def parse_data(input_data):
    data = [tuple(line.split('-')) for line in input_data.split('\n')]
    graph = nx.Graph()
    graph.add_edges_from(data)
    return graph


def part_a(input_data):
    graph = parse_data(input_data)
    cliques = nx.enumerate_all_cliques(graph)
    return len([c for c in cliques if len(c) == 3 and any(d.startswith('t') for d in c)])


def part_b(input_data):
    graph = parse_data(input_data)
    cliques = list(nx.find_cliques(graph))
    return ','.join(sorted(max(cliques, key=len)))


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
