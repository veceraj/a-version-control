import config

ADD = "add"
REMOVE = "remove"


def removeRestFirst(first: list, changes: list, i, j, is_print: bool) -> list:
    while i < len(first):
        is_print and config.print_remove(first[i])
        changes.append((REMOVE, j, None))
        i += 1

    return changes


def addRestSecond(second: list, changes: list, i, j, is_print: bool) -> list:
    numAdded = 0
    while j < len(second):
        is_print and config.print_add(second[j])
        changes.append((ADD, i + numAdded, second[j]))
        j += 1
        numAdded += 1

    return changes


def findInSecondFromIndex(line, second, j) -> int | None:
    found = False
    foundIndex = None

    for k in range(j, len(second)):
        if found:
            continue

        if line == second[k]:
            found = True
            foundIndex = k

    return foundIndex


def diff(first: list, second: list, is_print: bool = False) -> list:
    changes = []
    i, j = 0, 0
    numAdded, numRemoved = 0, 0

    while i < len(first):
        if j >= len(second):
            # if end of second reached
            return removeRestFirst(first, changes, i, j, is_print)

        if first[i] == second[j]:
            is_print and config.print_equal(first[i])
            i += 1
            j += 1
            continue

        foundIndex = findInSecondFromIndex(first[i], second, j)

        if foundIndex == None:
            is_print and config.print_remove(first[i])
            changes.append((REMOVE, i - numRemoved + numAdded, None))
            i += 1
            numRemoved += 1
        else:
            localNumAdded = 0
            for k in range(j, foundIndex):
                is_print and config.print_add(second[k])
                changes.append((ADD, j + localNumAdded, second[k]))
                localNumAdded += 1

            numAdded += localNumAdded
            j = foundIndex

    # if second remains
    return addRestSecond(second, changes, i, j, is_print)
