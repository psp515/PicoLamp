from ujson import loads


def read_json(filename: str):
    return_data = None

    with open(filename) as file:
        data = file.read()
        string_data = str(data)
        return_data = loads(string_data)

    return return_data
