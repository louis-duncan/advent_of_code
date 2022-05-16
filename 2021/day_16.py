import binascii
from typing import Optional
from math import prod

test_data = """A0016C880162017C3686B18A3D4780"""
real_data = """220D700071F39F9C6BC92D4A6713C737B3E98783004AC0169B4B99F93CFC31AC4D8A4BB89E9D654D216B80131DC0050B20043E27C1F83240086C468A311CC0188DB0BA12B00719221D3F7AF776DC5DE635094A7D2370082795A52911791ECB7EDA9CFD634BDED14030047C01498EE203931BF7256189A593005E116802D34673999A3A805126EB2B5BEEBB823CB561E9F2165492CE00E6918C011926CA005465B0BB2D85D700B675DA72DD7E9DBE377D62B27698F0D4BAD100735276B4B93C0FF002FF359F3BCFF0DC802ACC002CE3546B92FCB7590C380210523E180233FD21D0040001098ED076108002110960D45F988EB14D9D9802F232A32E802F2FDBEBA7D3B3B7FB06320132B0037700043224C5D8F2000844558C704A6FEAA800D2CFE27B921CA872003A90C6214D62DA8AA9009CF600B8803B10E144741006A1C47F85D29DCF7C9C40132680213037284B3D488640A1008A314BC3D86D9AB6492637D331003E79300012F9BDE8560F1009B32B09EC7FC0151006A0EC6082A0008744287511CC0269810987789132AC600BD802C00087C1D88D05C001088BF1BE284D298005FB1366B353798689D8A84D5194C017D005647181A931895D588E7736C6A5008200F0B802909F97B35897CFCBD9AC4A26DD880259A0037E49861F4E4349A6005CFAD180333E95281338A930EA400824981CC8A2804523AA6F5B3691CF5425B05B3D9AF8DD400F9EDA1100789800D2CBD30E32F4C3ACF52F9FF64326009D802733197392438BF22C52D5AD2D8524034E800C8B202F604008602A6CC00940256C008A9601FF8400D100240062F50038400970034003CE600C70C00F600760C00B98C563FB37CE4BD1BFA769839802F400F8C9CA79429B96E0A93FAE4A5F32201428401A8F508A1B0002131723B43400043618C2089E40143CBA748B3CE01C893C8904F4E1B2D300527AB63DA0091253929E42A53929E420"""


class DataStream:
    def __init__(self, data: str):
        self.data = data
        self.data_size = len(data)
        self.pos = 0

    @property
    def data_remaining(self) -> int:
        return self.data_size - (self.pos + 1)

    def get_chunk(self, size: int) -> Optional[str]:
        if self.data_remaining:
            chunk = self.data[self.pos: self.pos + size]
            self.pos += size
            return chunk
        else:
            return None

    @property
    def next_byte(self):
        return self.data[self.pos: self.pos + 8]


def decode_type_4(version: int, data: DataStream) -> dict:
    done = False
    bits = ""
    while not done:
        chunk = data.get_chunk(5)
        bits += chunk[1:]
        if chunk[0] == "0":
            done = True
    return {"value": int(bits, 2)}


def decode_op(version: int, type_id: int, data: DataStream) -> dict:
    length_type = int(data.get_chunk(1))
    if length_type == 0:
        length_bits = data.get_chunk(15)
        children_length = int(length_bits, 2)
        children_data_stream = DataStream(data.get_chunk(children_length))
        children = list(packets(children_data_stream))
    elif length_type == 1:
        num_children = int(data.get_chunk(11), 2)
        children = [decode_next_packet(data) for _ in range(num_children)]
    else:
        raise ValueError("Invalid OP length code.")
    return {"children": children}


def decode_next_packet(data: DataStream) -> dict:
    version = int(data.get_chunk(3), 2)
    type_id = int(data.get_chunk(3), 2)

    packet = {
        "version": version,
        "type_id": type_id
    }
    match type_id:
        case 4:
            packet = packet | decode_type_4(version, data)
        case _:
            packet = packet | decode_op(version, type_id, data)

    return packet


def packets(data: DataStream):
    while data.data_remaining > 6:
        yield decode_next_packet(data)


def get_version_count(packet: dict):
    count = packet["version"]
    if children := packet.get("children"):
        for child in children:
            count += get_version_count(child)
    return count


def resolve_packet(packet):
    type_id = packet["type_id"]
    match type_id:
        case 0:
            # Sum
            return sum([resolve_packet(child) for child in packet["children"]])
        case 1:
            # product
            return prod([resolve_packet(child) for child in packet["children"]])
        case 2:
            # min
            return min([resolve_packet(child) for child in packet["children"]])
        case 3:
            # max
            return max([resolve_packet(child) for child in packet["children"]])
        case 4:
            # static
            return packet["value"]
        case 5:
            # ge
            return int(resolve_packet(packet["children"][0])) > int(resolve_packet(packet["children"][1]))
        case 6:
            # le
            return int(resolve_packet(packet["children"][0])) < int(resolve_packet(packet["children"][1]))
        case 7:
            # eq
            return int(resolve_packet(packet["children"][0])) == int(resolve_packet(packet["children"][1]))
        case _:
            # Raise
            raise ValueError(f"Packets with invalid {type_id=}")


def main():
    global test_data, real_data
    data = real_data

    binary_string = "".join((str(bin(b)).split("b")[1].zfill(8) for b in binascii.unhexlify(data)))
    data = DataStream(binary_string)

    for packet in packets(data):
        print(packet)
        print("Sum:", resolve_packet(packet))


if __name__ == '__main__':
    main()
