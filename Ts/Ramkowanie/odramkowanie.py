import crcmod

FLAG = '01111110'
GENERATOR_POLY = 0x107  # CRC-8: x^8 + x^2 + x + 1

def bit_unstuffing(bits: str) -> str:
    result = ""
    count = 0
    i = 0
    while i < len(bits):
        result += bits[i]
        if bits[i] == '1':
            count += 1
            if count == 5:
                i += 1  # pomiń sztucznie wstawione 0
                count = 0
        else:
            count = 0
        i += 1
    return result

def check_crc(bits: str) -> bool:
    if len(bits) < 8:
        return False
    crc_func = crcmod.mkCrcFun(GENERATOR_POLY, initCrc=0, rev=False)
    data_bits = bits[:-8]
    crc_bits = bits[-8:]
    try:
        data_bytes = int(data_bits, 2).to_bytes((len(data_bits) + 7) // 8, byteorder='big')
        computed_crc = crc_func(data_bytes)
        return format(computed_crc, '08b') == crc_bits
    except Exception:
        return False

def main():
    with open("W", "r") as fin:
        raw_data = ''.join(line.strip() for line in fin)  # całość jako jeden ciąg bitów

    recovered_bits = ""
    errors = []
    valid_frames = 0
    idx = 0
    frame_number = 1

    while idx < len(raw_data):
        start_idx = raw_data.find(FLAG, idx)
        if start_idx == -1:
            break
        end_idx = raw_data.find(FLAG, start_idx + len(FLAG))
        if end_idx == -1:
            break
        frame_data = raw_data[start_idx + len(FLAG):end_idx]
        idx = end_idx + len(FLAG)

        unstuffed = bit_unstuffing(frame_data)
        if check_crc(unstuffed):
            recovered_bits += unstuffed[:-8]  # usuń CRC
            valid_frames += 1
        else:
            errors.append(f"Ramka {frame_number}: błędne CRC - ramka odrzucona.")
        frame_number += 1

    with open("Z_odtworzony", "w") as fout:
        fout.write(recovered_bits)

    with open("bledne_ramki.log", "w") as ferr:
        for err in errors:
            ferr.write(err + '\n')

    print(f"Poprawnie odczytano {valid_frames} ramek. Odrzucono {len(errors)} ramek.")
    if errors:
        print("Szczegóły znajdziesz w pliku 'bledne_ramki.log'.")

if __name__ == "__main__":
    main()
