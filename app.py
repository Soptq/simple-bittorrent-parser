import bencoding
from utils import *


def read_metainfo(filepath):
    with open(filepath, 'rb') as f:
        metainfo = bencoding.bdecode(f.read())

    if metainfo is None:
        raise Exception("Metainfo read failed.")

    encoding = metainfo[b"encoding"] if b"encoding" in metainfo else b"utf-8"

    announce = meta_decode(metainfo[b"announce"], encoding)

    creation_date = meta_decode(metainfo[b"creation date"], encoding) \
        if b"creation data" in metainfo else None
    creator = meta_decode(metainfo[b"created by"], encoding) \
        if b"created by" in metainfo else None
    comment = meta_decode(metainfo[b"comment"], encoding) \
        if b"comment" in metainfo else None
    announce_list = meta_decode(metainfo[b"announce-list"], encoding) \
        if b"announce-list" in metainfo else None

    piece_length = meta_decode(metainfo[b"info"][b"piece length"], encoding)
    pieces = metainfo[b"info"][b"pieces"]
    private = meta_decode(metainfo[b"info"][b"private"], encoding) \
        if b"private" in metainfo[b"info"] else 0

    single_file_mode = b"files" not in metainfo[b"info"]
    name = meta_decode(metainfo[b"info"][b"name"], encoding)
    files = []
    if single_file_mode:
        tfile = {"length": meta_decode(metainfo[b"info"][b"length"], encoding),
                 "md5sum": meta_decode(metainfo[b"info"][b"md5sum"], encoding) \
                     if b"md5sum" in metainfo[b"info"] else None,
                 "path": None}
        files.append(tfile)
    else:
        for tf in metainfo[b"info"][b"files"]:
            tfile = {"length": meta_decode(tf[b"length"], encoding),
                     "md5sum": meta_decode(tf[b"md5sum"], encoding) \
                         if b"md5sum" in tf else None,
                     "path": meta_decode(tf[b"path"], encoding)}
            files.append(tfile)

    return {
        "announce": announce,
        "cdate": creation_date,
        "creator": creator,
        "comment": comment,
        "announce_list": announce_list,
        "single_file": single_file_mode,
        "piece_length": piece_length,
        "pieces": pieces,
        "private": private,
        "name": name,
        "files": files
    }





if __name__ == "__main__":
    meta_data = read_metainfo("file.torrent")
    metainfo_fmt(meta_data)
