def squash(seq):
    value = seq

    if isinstance(value, (list, tuple)) and len(value) == 1:
        value = value[0]

    return value


def sequencify(value, type_=list):
    if not isinstance(value, (list, tuple)):
        value = list([value])

    value = type_(value)

    return value
