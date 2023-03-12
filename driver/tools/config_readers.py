from ujson import loads
from models.color import Color


def read_json(filename: str):
    return_data = None

    with open(filename) as file:
        data = file.read()
        string_data = str(data)
        return_data = loads(string_data)

    return return_data


def read_colors(filename: str):
    data = read_json(filename)
    colors = [Color(x["r"], x["g"], x["b"], x["name"]) for x in data["colors"]]
    return colors
