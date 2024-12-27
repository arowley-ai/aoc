import itertools
import aocd
import martens as mt
import re
import random

pattern = r"(\w+) (AND|XOR|OR) (\w+) -> (\w+)"


def parse_data(input_data):
    state_raw_data, instructions_raw_data = input_data.split('\n\n')
    state_data = mt.Dataset(dict(line=state_raw_data.split('\n'))) \
        .mutate_stretch(lambda line: line.split(': '), ['wire', 'value']) \
        .replace(int, ['value']).replace(bool, ['value']) \
        .drop(['line'])
    instructions_data = mt.Dataset(dict(line=instructions_raw_data.split('\n'))) \
        .mutate_stretch(lambda line: list(re.match(pattern, line).groups()), ['wire_a', 'switch', 'wire_b', 'wire_c']) \
        .drop(['line'])
    return state_data, instructions_data


def evaluate(state_data, instructions_data):
    states = {wire: value for wire, value in state_data.generator(state_data.columns)}
    instructions = set(instructions_data.generator(instructions_data.columns))
    while len(instructions) > 0:
        new_instructions = {i for i in instructions if i[0] in states and i[2] in states}
        instructions = instructions - new_instructions
        if len(new_instructions) == 0:
            return -1
        for wire_a, switch, wire_b, wire_c in new_instructions:
            if switch == 'AND':
                states[wire_c] = states[wire_a] and states[wire_b]
            elif switch == 'OR':
                states[wire_c] = states[wire_a] or states[wire_b]
            else:
                states[wire_c] = states[wire_a] ^ states[wire_b]
    matched_states = {state for state in states if re.fullmatch(pattern=r'z\d{2}', string=state)}
    return sum(2 ** int(s[1:]) for s in matched_states if states[s])


def part_a(input_data):
    state_data, instructions_data = parse_data(input_data)
    return evaluate(state_data, instructions_data)


def get_xy_ancestors(value, instruction_map):
    ancestors = instruction_map[value]
    while not all(a not in instruction_map for a in ancestors):
        ancestors = [y for a in ancestors for y in (instruction_map[a] if a in instruction_map else [a])]
    return sorted(set(ancestors))


def describe(input_data):
    state_data, instructions_data = parse_data(input_data)
    instruction_map = {wire_c: [wire_a, wire_b] for wire_a, wire_b, wire_c in instructions_data.generator(['wire_a', 'wire_b', 'wire_c'])}
    all_ancestor_data = instructions_data.rename_and_select({'wire_c': 'value', 'switch': 'switch'}) \
        .mutate(lambda value: get_xy_ancestors(value=value, instruction_map=instruction_map), 'ancestors') \
        .replace(len, ['ancestors']).group_by(['switch', 'ancestors'], other_cols=['value'], count='count')
    print(all_ancestor_data)


def do_trial(instructions_data):
    trial_values = [[random.choice([True, False]) for _ in range(45)] for _ in range(2)]
    check_sum = sum(2 ** i for n in trial_values for i, v in enumerate(n) if v)
    wires = [f"{z}{k:02}" for z in ['x', 'y'] for k in range(45)]
    values = trial_values[0] + trial_values[1]
    state_data = mt.Dataset(dict(wire=wires, value=values))
    return evaluate(state_data, instructions_data) == check_sum


def do_trials(instructions_data, permute, fixes, trials):
    fixes_copy = fixes.copy()
    fixes_copy[permute[0]] = permute[1]
    fixes_copy[permute[1]] = permute[0]
    instructions_data_fixed = instructions_data.mutate(lambda wire_c: fixes_copy[wire_c] if wire_c in fixes_copy else wire_c, 'wire_c')
    return sum([do_trial(instructions_data_fixed) for _ in range(trials)])


def part_b(input_data, fixes):
    trials = 10
    state_data, instructions_data = parse_data(input_data)
    swappable = [wire for wire in instructions_data['wire_c'] if wire not in fixes]
    data = mt.Dataset(dict(permute=list(itertools.permutations(swappable, 2)))) \
        .mutate(lambda permute: do_trials(instructions_data, permute, fixes, trials), 'test')
    return ','.join(sorted(list(data.filter(trials, 'test')['permute'][0]) + list(fixes)))


day, year = aocd.get_day_and_year()
puzzle = aocd.models.Puzzle(day=day, year=year)
puzzle_input_data = aocd.get_data(day=day, year=year)

example_input = puzzle.examples[0].input_data
second_example = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""

third_example = """x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z00"""

part_a_example = part_a(example_input)
print(part_a_example)

part_a_example = part_a(second_example)
print(part_a_example)

part_a_answer = part_a(puzzle_input_data)
print(part_a_answer)

# Note: I used the describe function to get the values of the first set of fixes to use below, it's obvious based on output of that
# describe(puzzle_input_data)
part_b_answer = part_b(puzzle_input_data, fixes={'fkb': 'z16', 'z16': 'fkb', 'rrn': 'z37', 'z37': 'rrn', 'rdn': 'z31', 'z31': 'rdn'})
print(part_b_answer)
