import aocd
import martens as mt
import aocar


def parse_data(input_data):
    data = mt.Dataset({'size': list(input_data)}).with_id('row_id') \
        .mutate(lambda row_id: int(row_id / 2) if row_id % 2 == 0 else None, 'data') \
        .drop(['row_id']) \
        .replace(int, ['size'])
    return data


def part_a(input_data):
    raw_data = parse_data(input_data)
    size, data = (raw_data[c] for c in raw_data.columns)
    while any(d is None for d in data):
        from_size = size[-1]
        from_data = data[-1]
        to_slot = min([r for r, d in enumerate(data) if d is None])
        to_size = size[to_slot]
        if to_size > from_size:
            data = data[0:to_slot] + [from_data] + data[to_slot:-2]
            size = size[0:to_slot] + [from_size] + [to_size - from_size] + size[to_slot + 1:-2]
        elif to_size < from_size:
            data[to_slot] = data[-1]
            size[-1] = from_size - to_size
        else:
            data[to_slot] = data[-1]
            data = data[:-2]
            size = size[:-2]
    finalised = mt.Dataset({'size': size, 'data': data}) \
        .rolling_mutate(lambda size: sum(size), name='rolling') \
        .mutate(lambda size, data, rolling: data * sum(list(range(rolling - size, rolling))), 'checksum')
    return sum(finalised['checksum'])


def part_b(input_data):
    raw_data = parse_data(input_data)
    size, data = (raw_data[c] for c in raw_data.columns)
    for record in sorted(set([r for r in data if r is not None]), reverse=True):
        from_slot = data.index(record)
        from_size = size[from_slot]
        from_data = data[from_slot]
        if any(d is None and s >= from_size for d, s in zip(data, size)):
            to_slot = min(i for s, d, i in zip(size, data, range(len(size))) if d is None and s >= from_size)
            to_size = size[to_slot]
            if to_slot < from_slot:
                if to_size > from_size:
                    data[from_slot] = None
                    data = data[0:to_slot] + [from_data] + data[to_slot:]
                    size = size[0:to_slot] + [from_size] + [to_size - from_size] + size[to_slot + 1:]
                else:
                    data[to_slot] = data[from_slot]
                    data[from_slot] = None
    finalised = mt.Dataset({'size': size, 'data': data}) \
        .rolling_mutate(lambda size: sum(size), name='rolling') \
        .mutate(lambda size, data, rolling: (data if data is not None else 0) * sum(list(range(rolling - size, rolling))), 'checksum')
    return sum(finalised['checksum'])


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

part_b_example = part_b(puzzle_input_data)
print(part_b_example)
