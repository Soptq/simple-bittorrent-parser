import Bencoding

with open('file.torrent', 'rb') as f:
    meta_info = f.read()
    torrent = Bencoding.bdecode(meta_info)
    print(torrent)