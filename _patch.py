ADD = "add"
REMOVE = "remove"


def add(data: list, line: int, payload):
    return data.insert(line, payload)


def remove(data: list, line: int):
    return data.pop(line)


def patch(original: list, log: list) -> list:
    data = original.copy()

    for operation, line, payload in log:
        if operation == REMOVE:
            remove(data, line)
        elif operation == ADD:
            add(data, line, payload)

    return data
