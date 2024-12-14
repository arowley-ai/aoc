import aocd
import martens as mt

adjacency_generator = [(-1, 0), (0, 1), (1, 0), (0, -1)]
adjacency_map = {
    (-1, 0): 'u',
    (0, 1): 'r',
    (1, 0): 'd',
    (0, -1): 'l'
}


def fence(coord, grid_size):
    rtn = []
    if coord[0] == 0:
        rtn += [(-1, 0)]
    if coord[0] == grid_size - 1:
        rtn += [(1, 0)]
    if coord[1] == 0:
        rtn += [(0, -1)]
    if coord[1] == grid_size - 1:
        rtn += [(0, 1)]
    return rtn


def divide_region(data):
    big_grid = [(coord, adjacency) for coord, adjacency in data.generator(['coord', 'adjacency'])]
    regions = []
    while sum(len(r) for r in regions) < len(big_grid):
        something_added = False
        for coord, adjacency in big_grid:
            if coord not in [r for region in regions for r in region]:
                for region in regions:
                    if any(r in adjacency for r in region) and coord not in region:
                        region.append(coord)
                        something_added = True
                        break
            if something_added:
                break
        if not something_added and len(big_grid) > 0:
            regions.append([next(coord for coord, adjacency in big_grid if coord not in [r for region in regions for r in region])])
    return regions


def parse_data(input_data):
    data = mt.Dataset({'line': [x for x in input_data.split('\n')]}) \
        .with_id('row_id') \
        .column_stack('line', enumeration='col_id') \
        .rename({'line': 'value'}) \
        .mutate(lambda row_id, col_id: (row_id, col_id), 'coord') \
        .mutate(lambda coord: [(coord[0] + a[0], coord[1] + a[1]) for a in adjacency_generator], 'adjacency')
    grid_size = max(data['col_id'] + data['row_id']) + 1
    regions, letters = zip(*[(r, letter) for letter in list(set(data['value'])) for r in divide_region(data.filter(letter, 'value'))])
    region_data = mt.Dataset({'value': list(letters), 'region': list(regions)}) \
        .with_id('region_id') \
        .mutate(lambda region: len(region), 'region_area')
    outer_fences = region_data \
        .with_constant(grid_size, 'grid_size') \
        .column_stack('region', new_name='coord') \
        .mutate_stack(fence) \
        .select(['region_id', 'coord', 'fence'])
    inner_fences = region_data.column_stack('region', new_name='coord') \
        .merge(data, how='inner', on=['coord', 'value']) \
        .select(['region_id', 'value', 'coord', 'adjacency']) \
        .column_stack('adjacency') \
        .merge(data.rename_and_select({'coord': 'adjacency', 'value': 'adjacent_value'}), how='inner', on=['adjacency']) \
        .filter(lambda value, adjacent_value: value != adjacent_value) \
        .mutate(lambda adjacency, coord: (adjacency[0] - coord[0], adjacency[1] - coord[1]), 'fence') \
        .select(['region_id', 'coord', 'fence'])
    fences = mt.stack([inner_fences, outer_fences]).select(['region_id', 'coord', 'fence'])
    return data, region_data, fences


def part_a(input_data):
    data, region_data, fences = parse_data(input_data)
    rtn_data = fences.group_by(['region_id'], other_cols=['fence']).replace(len, ['fence']) \
        .merge(region_data, how='inner', on=['region_id']) \
        .mutate(lambda region_area, fence: region_area * fence, 'price')
    return sum(rtn_data['price'])


def get_fence_groups(data):
    fence_groups = []
    fence_grid = [(coord, fence, adjacency) for coord, fence, adjacency in data.generator(['coord', 'fence', 'adjacency'])]
    while sum(len(f) for f in fence_groups) < len(fence_grid):
        for coord, fence, adjancency in fence_grid:
            added = False
            if all((fence,) + coord not in fence_group for fence_group in fence_groups):
                for fence_group in fence_groups:
                    if any((fence,) + a in fence_group for a in adjancency):
                        fence_group.append((fence,) + coord)
                        added = True
                        break
            if not added:
                fence_groups.append([(fence,) + coord])
    return fence_groups


def part_b(input_data):
    data, region_data, fences_raw = parse_data(input_data)
    fences = fences_raw.mutate(lambda fence: adjacency_map[fence], 'fence') \
        .mutate(lambda coord: [(coord[0] + a[0], coord[1] + a[1]) for a in adjacency_generator], 'adjacency') \
        .sort(['region_id', 'coord', 'fence'])
    region_ids = sorted(set(fences['region_id']))
    fence_groups = [
        get_fence_groups(fences.filter(region_id, 'region_id').drop(['region_id']))
        for region_id in region_ids]

    rtn_data = mt.Dataset({'region_id': region_ids, 'fence_groups': fence_groups}) \
        .replace(len, ['fence_groups']) \
        .merge(region_data, how='inner', on=['region_id']) \
        .mutate(lambda region_area, fence_groups: region_area * fence_groups, 'price')
    return sum(rtn_data['price'])


day, year = aocd.get_day_and_year()
puzzle = aocd.models.Puzzle(day=day, year=year)
puzzle_input_data = aocd.get_data(day=day, year=year)

example_input = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

# part_a_example = part_a(example_input)
# print(part_a_example)
#
# part_a_answer = part_a(puzzle_input_data)
# print(part_a_answer)

part_b_example = part_b(example_input)
print(part_b_example)

part_b_answer = part_b(puzzle_input_data)
print(part_b_answer)
