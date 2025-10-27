import crcmod

FLAG = '01111110'
GENERATOR_POLY = 0x107  # CRC-8: x^8 + x^2 + x + 1
LENGTH = 100
def bit_stuffing(bits: str) -> str:
    result = ""
    count = 0
    for bit in bits:
        result += bit
        if bit == '1':
            count += 1
            if count == 5:
                result += '0'  # dodaj 0 po pięciu jedynkach
                count = 0
        else:
            count = 0
    return result

def calculate_crc(bits: str) -> str:
    crc_func = crcmod.mkCrcFun(GENERATOR_POLY, initCrc=0, rev=False)
    data_bytes = int(bits, 2).to_bytes((len(bits) + 7) // 8, byteorder='big')
    crc = crc_func(data_bytes)
    return format(crc, '08b')

def split_into_blocks(bits: str, block_size: int = 100) -> list[str]:
    return [bits[i:i + block_size] for i in range(0, len(bits), block_size)]

def main():
    with open("Z", "r") as fin:
        raw_bits = fin.read().strip()

    blocks = split_into_blocks(raw_bits, LENGTH)
    framed_blocks = []

    for block in blocks:
        crc = calculate_crc(block)
        full_block = block + crc
        stuffed = bit_stuffing(full_block)
        framed = FLAG + stuffed + FLAG
        framed_blocks.append(framed)

    with open("W", "w") as fout:
        for frame in framed_blocks:
            fout.write(frame)

    print(f"Zapisano {len(framed_blocks)} ramek do pliku 'W'.")

if __name__ == "__main__":
    main()
