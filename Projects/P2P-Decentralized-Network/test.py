import torrent_parser as tp

def decode_torrent(torrent_path):
    data = tp.parse_torrent_file(torrent_path)
    return data
torrent_data = decode_torrent("age.torrent")
print(torrent_data['info']['name'])



decode_torrent("age.torrent")
