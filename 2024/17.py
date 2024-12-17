import random
import aocd
import re
import martens as mt

from dataclasses import dataclass, field

# from matplotlib import pyplot as plt


@dataclass
class Register:
    a: int
    b: int
    c: int
    position: int = 0
    output: list = field(default_factory=list)

    def run_program(self, program):
        self.position = 0
        while self.position < len(program):
            self.position = self.step(program[self.position], program[self.position + 1])

    def step(self, opcode, operand):
        if opcode == 0:
            return self.adv(operand)
        elif opcode == 1:
            return self.bxl(operand)
        elif opcode == 2:
            return self.bst(operand)
        elif opcode == 3:
            return self.jnz(operand)
        elif opcode == 4:
            return self.bxc()
        elif opcode == 5:
            return self.out(operand)
        elif opcode == 6:
            return self.bdv(operand)
        elif opcode == 7:
            return self.cdv(operand)

    def combo(self, operand):
        if operand < 4:
            return operand
        elif operand == 4:
            return self.a
        elif operand == 5:
            return self.b
        elif operand == 6:
            return self.c
        elif operand == 7:
            raise Exception('Illegal operand')
        else:
            raise Exception('Invalid operand')

    def adv(self, operand):
        self.a = self.a // 2 ** self.combo(operand)
        return self.position + 2

    def bxl(self, operand):
        self.b = self.b ^ operand
        return self.position + 2

    def bst(self, operand):
        self.b = self.combo(operand) % 8
        return self.position + 2

    def jnz(self, operand):
        if self.a != 0:
            return operand
        else:
            return self.position + 2

    def bxc(self):
        self.b = self.b ^ self.c
        return self.position + 2

    def out(self, operand):
        self.output.append(self.combo(operand) % 8)
        return self.position + 2

    def bdv(self, operand):
        self.b = self.a // 2 ** self.combo(operand)
        return self.position + 2

    def cdv(self, operand):
        self.c = self.a // 2 ** self.combo(operand)
        return self.position + 2

    @property
    def output_string(self):
        return ','.join(str(o) for o in self.output)


def list_of_numbers(line):
    return [int(m.group()) for m in re.finditer(r'\b\d+\b', line)]


def parse_data(input_data):
    lines = [x for x in input_data.split('\n')]
    register = Register(*[int(l.split(' ')[2]) for l in lines[0:3]])
    program = list_of_numbers(lines[4].split(' ')[1])
    return register, program


def part_a(input_data):
    register, program = parse_data(input_data)
    register.run_program(program)
    return register.output_string


def compute(input_data, a):
    register, program = parse_data(input_data)
    register.a = a
    register.run_program(program)
    return register, program


def do_trials(input_data, lower, upper, trials=1000):
    values = [lower, upper] + list(random.choices(range(lower, upper + 1), k=trials)) if upper - lower > trials else list(range(lower, upper + 1))
    return mt.Dataset({'value': values}) \
        .mutate(lambda value: compute(input_data, value)[0].output, 'output')


def get_bound(input_data, transform, output, lower, upper):
    while lower + 1 != upper:
        analysis = do_trials(input_data, lower, upper)
        bounds = analysis.replace(transform, ['output']).filter(output, 'output').group_by(['value'])['value']
        lower, upper = max(v for v in analysis['value'] if v < min(bounds)), min(bounds)
    return upper


def get_bounds(input_data, transform, bounds):
    program = compute(input_data, a=1)[1]
    analysis = do_trials(input_data, bounds[0], bounds[1])
    values = analysis.replace(transform, ['output']).sort(['value'])
    bounds_data = values.window_mutate(lambda output: output[-1] != output[0], window=2, name='boundary') \
        .window_mutate(lambda value: value[0], window=2, name='previous_value') \
        .window_mutate(lambda output: output[0], window=2, name='previous_output') \
        .filter(True, 'boundary') \
        .mutate(lambda output, value, previous_value: get_bound(input_data, transform, output, lower=previous_value, upper=value), 'bound')
    if bounds_data.record_length == 0:
        return [bounds] if values['output'][0] == transform(program) else []
    prior_output = bounds_data['previous_output'][0]
    prior_bound = bounds[0]
    all_bounds = []
    all_outputs = []
    for output, bound in bounds_data.generator(['output', 'bound']):
        all_outputs.append(prior_output)
        all_bounds.append((prior_bound, bound - 1))
        prior_output = output
        prior_bound = bound
    all_outputs.append(prior_output)
    all_bounds.append((prior_bound - 1, bounds[1]))
    return mt.Dataset({'output': all_outputs, 'bounds': all_bounds}).filter(transform(program), 'output')['bounds']


def part_b(input_data, bounds):
    register, program = parse_data(input_data)
    bounds = get_bounds(input_data, len, bounds)
    index = len(program) - 1
    while index > 0:
        # print(f'Trying index {index}')
        bounds = [b for bound in bounds for b in get_bounds(input_data, lambda k: k[index], bound)]
        index -= 1
    return min([a for bound in bounds for a in range(*bound) if compute(input_data, a)[0].output == program])


day, year = aocd.get_day_and_year()
puzzle = aocd.models.Puzzle(day=day, year=year)
puzzle_input_data = aocd.get_data(day=day, year=year)

example_input = puzzle.examples[0].input_data
example_input_b = """Register A: 1
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""


part_a_example = part_a(example_input)
print(part_a_example)

part_a_answer = part_a(puzzle_input_data)
print(part_a_answer)

part_b_example = part_b(example_input_b, bounds=(0, 10000000))
print(part_b_example)

part_b_answer = part_b(puzzle_input_data, bounds=[int(1E13), int(3E14)])
print(part_b_answer)


# def digit_analysis(input_data, lower, upper):
#     _, program = parse_data(input_data)
#     analysis = mt.Dataset({'value': list(random.choices(range(lower, upper), k=1000))}) \
#         .mutate(lambda value: compute(input_data, value)[0].output, 'output')
#     fig, axes = plt.subplots(4, 4, figsize=(12, 12))
#     for n, ax in enumerate(axes.flat):
#         scatter_colors = [y[n] for y in analysis['output']]
#         ax.scatter(analysis['value'], scatter_colors, alpha=0.5, s=10, c=scatter_colors, cmap='viridis')
#         ax.set_title(f"Scatter {n + 1}", fontsize=10)
#         ax.grid(True, linestyle='--', alpha=0.5)
#     plt.tight_layout()
#     plt.show()