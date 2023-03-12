from exception.setup_error import SetupError


def generate_groups(sizes: [], total_length: int):
    groups = []
    length = 0

    if len(sizes) == 0:
        SetupError("Invalid number of groups.")

    for size in sizes:
        groups.append([length + i for i in range(size)])
        length += size

    if length != total_length:
        SetupError("Invalid number of led-s in groups.")

    return groups