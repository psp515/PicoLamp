from ujson import loads


def read_json(filename: str):
    with open(filename) as file:
        data = file.read()
        string_data = str(data)
        parsed_data = loads(string_data)
        return parsed_data


def read_colors(filename: str):
    data = read_json(filename)
    colors = [[x["r"], x["g"], x["b"]] for x in data["colors"]]
    return colors
