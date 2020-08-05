import time


def bytesfmt(size):
    index = 0
    units = ["Bytes", "KB", "MB", "GB", "TB"]
    while size > 1024 and index < len(units):
        size /= 1024
        index += 1
    return f"{size:.3f} {units[index]}"


def meta_decode(data, encoding):
    if type(encoding) == bytes:
        encoding = encoding.decode("utf-8")

    if type(data) == bytes:
        return data.decode(encoding)

    if type(data) == list:
        transcode = []
        for d in data:
            transcode.append(meta_decode(d, encoding))
        return transcode

    if type(data) == dict:
        transcode = {}
        for dk, dv in data.items():
            transcode[meta_decode(dk, encoding)] = meta_decode(dv, encoding)
        return transcode

    return data


def metainfo_fmt(data):
    total_size = 0
    filepaths = []
    for tf in data["files"]:
        total_size += tf["length"]
        filepaths.append("/".join(tf["path"]))

    print("Basic Information of Selected Torrent File:")
    print(f"Creator: {data['creator'] if 'creator' in data else 'UNKNOWN'}\t"
          f"Created at: {time.ctime(data['cdate']) if 'cdate' in data else 'UNKNOWN'}\t"
          f"Size: {bytesfmt(total_size)}")
    print(f"Comment: {data['comment'] if 'comment' in data else 'NONE'}\t")
    print(f"Announce: {data['announce']}")
    print(f"Files:")
    for filepath in filepaths:
        print(f"\t{filepath}")


if __name__ == "__main__":
    print(bytesfmt(4650008))