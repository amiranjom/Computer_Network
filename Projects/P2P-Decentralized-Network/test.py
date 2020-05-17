import torrent_parser as tp
import hashlib
import bencoding
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

def decode_torrent(torrent_path):
    data = tp.parse_torrent_file(torrent_path)
    return data
torrent_data = decode_torrent("age.torrent")
print(torrent_data['info']['name'])
t = hashlib.sha1(bencoding.bencode(torrent_data['info'])).hexdigest()
print(t)


decode_torrent("age.torrent")

def test():
    with open("age.torrent") as f:
        raw_data = f.read()
        data = bencode.bdecode(raw_data)
        info_hash = hashlib.sha1(bencode.bencode(data['info'])).hexdigest()
        announce_hash = hashlib.sha1(bencode.bencode(data['announce'])).hexdigest()
        print(raw_data)
        print(data)
        print(info_hash)
        print(announce_hash)
    return 0
