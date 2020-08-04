def is_decimal(d):
    return ord("0") <= d <= ord("9")


def pair_integer(data, start):
    if data[start] != ord('i'):
        raise Exception("Bdecode failed: Pair integer failed")
    if data[start + 1] is ord("-") and data[start + 2] is ord("0"):
        raise Exception("Bdecode failed: Pair integer failed")
    if data[start + 1] is ord("0") and data[start + 2] is not ord("e"):
        raise Exception("Bdecode failed: Pair integer failed")

    index = start + 1
    while data[index] != ord("e"):
        if index is not start + 1 and not is_decimal(data[index]):
            raise Exception("Bdecode failed: Pair integer failed")
        index += 1
    return int(data[start + 1: index]), index + 1


def construct_integer(data):
    return f"i{str(data)}e".encode('utf-8')


def pair_str(data, start):
    if not is_decimal(data[start]):
        raise Exception("Bdecode failed: Pair string failed")

    index = start + 1
    while data[index] != ord(":"):
        if not is_decimal(data[index]):
            raise Exception("Bdecode failed: Pair string failed")
        index += 1
    str_length = int(data[start: index])
    return data[index + 1: index + str_length + 1], index + str_length + 1


def construct_str(data):
    return str(len(data)).encode('utf-8') + b":" + data


def pair_list(data, start):
    if data[start] != ord("l"):
        raise Exception("Bdecode failed: Pair list failed")

    blist = []
    index = start + 1
    while index < len(data):
        if data[index] == ord("e"):
            break
        if data[index] == ord("i"):
            bvalue, bend = pair_integer(data, index)
        if is_decimal(data[index]):
            bvalue, bend = pair_str(data, index)
        if data[index] == ord("l"):
            bvalue, bend = pair_list(data, index)
        if data[index] == ord("d"):
            bvalue, bend = pair_dict(data, index)
        blist.append(bvalue)
        index = bend
    return blist, index + 1


def construct_list(data):
    bstr = b"l"
    for item in data:
        if type(item) == int:
            bstr += construct_integer(item)
        if type(item) == bytes:
            bstr += construct_str(item)
        if type(item) == list:
            bstr += construct_list(item)
        if type(item) == dict:
            bstr += construct_dict(item)
    return bstr + b"e"


def pair_dict(data, start):
    if data[start] != ord("d"):
        raise Exception("Bdecode failed: Pair dict failed")

    current_pointer = "key"
    key_storage = None
    bdict = {}

    index = start + 1
    while index < len(data):
        if data[index] == ord("e"):
            break
        if data[index] == ord("i"):
            bvalue, bend = pair_integer(data, index)
        if is_decimal(data[index]):
            bvalue, bend = pair_str(data, index)
        if data[index] == ord("l"):
            bvalue, bend = pair_list(data, index)
        if data[index] == ord("d"):
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


def construct_dict(data):
    bstr = b"d"
    for items in data.items():
        for item in items:
            if type(item) == int:
                bstr += construct_integer(item)
            if type(item) == bytes:
                bstr += construct_str(item)
            if type(item) == list:
                bstr += construct_list(item)
            if type(item) == dict:
                bstr += construct_dict(item)
    return bstr + b"e"


def bdecode(data):
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
    if data[0] == ord("i"):
        return pair_integer(data, 0)[0]
    if data[0] == ord("l"):
        return pair_list(data, 0)[0]
    if data[0] == ord("d"):
        return pair_dict(data, 0)[0]


def bencode(data):
    if type(data) == int:
        return construct_integer(data)
    if type(data) == bytes:
        return construct_str(data)
    if type(data) == list:
        return construct_list(data)
    if type(data) == dict:
        return construct_dict(data)