def is_decimal(d):
    return "0" <= d <= "9"


def pair_integer(data, start):
    if data[start] != 'i':
        raise Exception("Bdecode failed: Pair integer failed")
    if data[start + 1] is "-" and data[start + 2] is "0":
        raise Exception("Bdecode failed: Pair integer failed")
    if data[start + 1] is "0" and data[start + 2] is not "e":
        raise Exception("Bdecode failed: Pair integer failed")

    index = start + 1
    while data[index] != "e":
        if index is not start + 1 and not is_decimal(data[index]):
            raise Exception("Bdecode failed: Pair integer failed")
        index += 1
    return int(data[start + 1: index]), index + 1


def pair_str(data, start):
    if not is_decimal(data[start]):
        raise Exception("Bdecode failed: Pair string failed")

    index = start + 1
    while data[index] != ":":
        if not is_decimal(data[index]):
            raise Exception("Bdecode failed: Pair string failed")
        index += 1
    str_length = int(data[start: index])
    return data[index + 1: index + str_length + 1], index + str_length + 1


def pair_list(data, start):
    if data[start] != "l":
        raise Exception("Bdecode failed: Pair list failed")

    blist = []
    index = start + 1
    while index < len(data):
        if data[index] == "e":
            break
        if data[index] == "i":
            bvalue, bend = pair_integer(data, index)
        if is_decimal(data[index]):
            bvalue, bend = pair_str(data, index)
        if data[index] == "l":
            bvalue, bend = pair_list(data, index)
        if data[index] == "d":
            bvalue, bend = pair_dict(data, index)
        blist.append(bvalue)
        index = bend
    return blist, index + 1


def pair_dict(data, start):
    if data[start] != "d":
        raise Exception("Bdecode failed: Pair dict failed")

    current_pointer = "key"
    key_storage = None
    bdict = {}

    index = start + 1
    while index < len(data):
        if data[index] == "e":
            break
        if data[index] == "i":
            bvalue, bend = pair_integer(data, index)
        if is_decimal(data[index]):
            bvalue, bend = pair_str(data, index)
        if data[index] == "l":
            bvalue, bend = pair_list(data, index)
        if data[index] == "d":
            bvalue, bend = pair_dict(data, index)

        index = bend

        if current_pointer == "key":
            key_storage = bvalue
            current_pointer = "value"
            continue
        if current_pointer == "value":
            bdict[key_storage] = bvalue
            current_pointer = "key"

    return bdict, index + 1


def bdecode(data: str):
    """
    Reference: https://wiki.theory.org/BitTorrentSpecification

    TL;DR:
    Byte Strings: <length>:<string>, e.g. 5:apple => "apple".
    Integer: i<value>e, e.g. i3e => 3. **Leading zero is invalid**
    Lists: l<value>e, e.g. l4:span4:eggse => ["span", "eggs"].
    Dictionary: d<value>e, e.g. d3:cow3:moo4:spam4:eggse => {"cow": "moo", "spam": "eggs"}

    :param data: the encoded data
    :return: the parsed data
    """
    if is_decimal(data[0]):
        return pair_str(data, 0)[0]
    if data[0] == "i":
        return pair_integer(data, 0)[0]
    if data[0] == "l":
        return pair_list(data, 0)[0]
    if data[0] == "d":
        return pair_dict(data, 0)[0]